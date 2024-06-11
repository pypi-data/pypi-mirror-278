import subprocess
import logging
import logging.config


def get_image_raw_topic():
    result = subprocess.run(
        ["ros2", "topic", "list"], stdout=subprocess.PIPE, text=True
    )
    topics = result.stdout.splitlines()

    for topic_name in topics:

        if "/camera/camera/color/image_raw" in topic_name:
            logging.info("Subscribed Topic is: ")
            logging.info(topic_name)
            return topic_name
        elif "/rgb/image_raw" in topic_name:
            logging.info("Subscribed Topic is: ")
            logging.info(topic_name)
            return topic_name

    return "/color/image_raw"

def get_depth_raw_topic():
    result = subprocess.run(
        ["ros2", "topic", "list"], stdout=subprocess.PIPE, text=True
    )
    topics = result.stdout.splitlines()

    for topic_name in topics:

        if "/camera/camera/aligned_depth_to_color/image_raw" in topic_name:
            logging.info("Subscribed Topic is: ")
            logging.info(topic_name)
            return topic_name
        elif "/oak/stereo/image_raw" in topic_name:
            logging.info("Subscribed Topic is: ")
            logging.info(topic_name)
            return topic_name
        
    return "/camera/camera/aligned_depth_to_color/image_raw"