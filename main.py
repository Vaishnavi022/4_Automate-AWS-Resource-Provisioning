import boto3
import logging
import time

# ---------------- CONFIG ----------------
REGION = "ap-south-1"
BUCKET_NAME = "disha-automation-bucket-12345"   # must be unique
USER_NAME = "automation-user"
KEY_NAME = "WebServer-Base-ec2"   # ✅ your key pair name (NO .pem)

# Logging setup
logging.basicConfig(level=logging.INFO)

# Clients
iam = boto3.client('iam')
s3 = boto3.client('s3', region_name=REGION)
ec2 = boto3.resource('ec2', region_name=REGION)


# ---------------- IAM USER ----------------
def create_iam_user():
    try:
        iam.create_user(UserName=USER_NAME)
        logging.info(f"IAM User Created: {USER_NAME}")
    except Exception as e:
        if "EntityAlreadyExists" in str(e):
            logging.warning("IAM user already exists")
        else:
            logging.error(f"IAM Error: {e}")


# ---------------- S3 BUCKET ----------------
def create_s3_bucket():
    try:
        s3.create_bucket(
            Bucket=BUCKET_NAME,
            CreateBucketConfiguration={'LocationConstraint': REGION}
        )
        logging.info(f"S3 Bucket Created: {BUCKET_NAME}")
    except Exception as e:
        if "BucketAlreadyOwnedByYou" in str(e):
            logging.warning("Bucket already exists")
        else:
            logging.error(f"S3 Error: {e}")


# ---------------- EC2 INSTANCE ----------------
def launch_ec2():
    try:
        instances = ec2.create_instances(
            ImageId='ami-0f58b397bc5c1f2e8',  # Amazon Linux
            MinCount=1,
            MaxCount=1,
            InstanceType='t2.micro',
            KeyName=KEY_NAME
        )

        instance = instances[0]
        instance_id = instance.id

        # Tagging
        instance.create_tags(
            Tags=[{'Key': 'Name', 'Value': 'AutoInstance'}]
        )

        logging.info(f"EC2 Instance Launched: {instance_id}")

    except Exception as e:
        if "InvalidKeyPair" in str(e):
            logging.error("Key pair not found. Check name & region.")
        else:
            logging.error(f"EC2 Error: {e}")


# ---------------- MAIN ----------------
def main():
    logging.info("Starting AWS Automation Project...")

    create_iam_user()
    time.sleep(2)

    create_s3_bucket()
    time.sleep(2)

    launch_ec2()

    logging.info("Automation Completed Successfully!")


if __name__ == "__main__":
    main()