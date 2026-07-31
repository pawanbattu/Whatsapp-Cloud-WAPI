from django.views import View
from django.http import StreamingHttpResponse
from WhatsPanel.models import *
from django.conf import settings
import pika
from core.logger import app_logs
import traceback

class MessageStreamView(View):
    def get(self, request, admin_id, *args, **kwargs):
        response = StreamingHttpResponse(
            self.event_generator(admin_id),
            content_type='text/event-stream'
        )

        response['Cache-Control'] = 'no-cache'
        response['X-Accel-Buffering'] = 'no'

        return response
    
    def event_generator(self, admin_id):
        connection = None
        try:
            params = pika.URLParameters(settings.CELERY_BROKER_URL)
            params.heartbeat = 30
            params.blocked_connection_timeout = 30

            connection = pika.BlockingConnection(params)
            channel = connection.channel()

            exchange_name = f'whatsapp_stream_{admin_id}'
            channel.exchange_declare(exchange=exchange_name, exchange_type='fanout')

            result = channel.queue_declare(queue='', exclusive=True)
            queue_name = result.method.queue
            channel.queue_bind(exchange=exchange_name, queue=queue_name)

            for method_frame, properties, body in channel.consume(queue_name, inactivity_timeout=15):
                if body:
                    payload = body.decode('utf-8')
                    yield f"data: {payload}\n\n"
                    channel.basic_ack(method_frame.delivery_tag)
                else:
                    yield ": keepalive\n\n"

        except GeneratorExit:
            # client disconnected / tab closed — normal, not an error
            app_logs("INFO", "SSE client disconnected for admin", {"admin_id": admin_id})
            raise
            
        except pika.exceptions.ConnectionClosedByBroker as e:
            # Broker restarted or forcefully closed the connection
            app_logs("WARNING", "RabbitMQ broker forced connection closure", {"admin_id": admin_id, "error": str(e)})
            yield f"event: error\ndata: {{\"message\": \"Broker disconnected\"}}\n\n"
            
        except pika.exceptions.AMQPConnectionError as e:
            # General connection failure (network drop, etc.)
            app_logs("WARNING", "RabbitMQ connection lost", {"admin_id": admin_id, "error": str(e)})
            yield f"event: error\ndata: {{\"message\": \"Stream connection lost\"}}\n\n"
            
        except Exception:
            # Actual unexpected code crashes
            app_logs("ERROR", "SSE stream crashed for admin", {"admin_id": admin_id, "error":  str(traceback.format_exc())})
            yield f"event: error\ndata: {{\"message\": \"Internal stream error\"}}\n\n"
            
        finally:
            try:
                if connection and connection.is_open:
                    connection.close()
            except Exception:
                app_logs("EXCEPTION", "Error closing pika connection for admin", {"admin_id": admin_id, "error":  str(traceback.format_exc())})