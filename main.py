import os
from google.cloud import storage


GCLOUD_PATH_TO_CREDENTIALS_FILE = os.environ.get('GCLOUD_PATH_TO_CREDENTIALS_FILE')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = GCLOUD_PATH_TO_CREDENTIALS_FILE

GCLOUD_PROJECT_ID = os.environ.get('GCLOUD_PROJECT_ID')
GCLOUD_STORAGE_BUCKET_NAME = os.environ.get('GCLOUD_STORAGE_BUCKET_NAME')


def list_gcloud_storage_buckets():
    storage_client = storage.Client()
    buckets = list(storage_client.list_buckets())

    return buckets # https://cloud.google.com/python/docs/reference/storage/latest/google.cloud.storage.bucket.Bucket#properties


def list_blobs_in_gcloud_storage_bucket(bucket_name):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blobs = list(bucket.list_blobs())

    return blobs # https://cloud.google.com/python/docs/reference/storage/latest/google.cloud.storage.blob.Blob#properties

def print_object_attributes(obj):
    print("Attributes of the object:")
    for attr in dir(obj):
        print("obj.%s = %r" % (attr, getattr(obj, attr)))


def upload_blob_to_gcloud_storage(bucket_name, source_file_name, destination_blob_name):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print("File {} uploaded to {}.".format(source_file_name, destination_blob_name))


def download_blob_from_gcloud_storage(bucket_name, source_blob_name, destination_file_name):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(source_blob_name)

    blob.download_to_filename(destination_file_name)

    print("Blob {} downloaded to {}.".format(source_blob_name, destination_file_name))


def main():
    # buckets = list_gcloud_storage_buckets()
    # blobs = list_blobs_in_gcloud_storage_bucket(GCLOUD_STORAGE_BUCKET_NAME)

    # print("#############################")
    # print_object_attributes(buckets[0])

    # print("#############################")
    # print_object_attributes(blobs[0])

    for i in range(0, 5):
        os.system(f"echo Hello World {i} > ./test.txt")
        upload_blob_to_gcloud_storage(GCLOUD_STORAGE_BUCKET_NAME, "./test.txt", f"uploaded_test_{i}.txt")

    blobs = list_blobs_in_gcloud_storage_bucket(GCLOUD_STORAGE_BUCKET_NAME)
    for blob in blobs:
        print(blob.name)
    
    for i in range(0, 5):
        download_blob_from_gcloud_storage(GCLOUD_STORAGE_BUCKET_NAME, f"uploaded_test_{i}.txt", f"./downloaded_test_{i}.txt")


if __name__ == "__main__":
    main()