from google.cloud import pubsub_v1

def publish_country_selection(country_name):
    publisher = pubsub_v1.PublisherClient()
    topic_path = "projects/gdp-dash/topics/gdp-dash-topic"
    message = f"Selected country: {country_name}"
    publisher.publish(topic_path, message.encode("utf-8"))