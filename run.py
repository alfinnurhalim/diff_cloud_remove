from pyngrok import ngrok
from apps import create_app
import apps.config as config

if __name__ == '__main__':
    # Start ngrok tunnel
    # ngrok.set_auth_token(config.NGROK_TOKEN)
    # public_url = ngrok.connect(config.PORT)
    # print(f"ngrok tunnel: {public_url}")

    # Create and run Flask app
    app = create_app()
    app.run(host="0.0.0.0", port=config.PORT)
