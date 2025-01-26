import os
import gridfs
from config import db

def upload_file(file_loc, file_name, fs):
    with open(file_loc, 'rb') as file_data:
        data = file_data.read()
    try:
        fid = fs.put(data, filename=file_name)
        print("upload complete")
        # TODO: payment status is updated to “completed”.
        # Generate a download link for the uploaded evidence file.
        #  return fid
    except Exception as e:
        print("Error in upload_file(): {e}")


def  download_file(download_loc, db, fs, file_name):
    data = db.files.files.find_one({"filename":file_name})
    print(data)
    fs_id = data['_id']
    out_data = fs.get(fs_id).read()

    with open(download_loc, 'wb') as output:
        output.write(out_data)

    print("Download Completed!")


file_name = "cst8101.pdf"
file_loc = "F:\Adcore_CRUD/" + file_name
down_loc = os.path.join(os.getcwd() + "/downloads/" + file_name)
# print(down_loc)
fs = gridfs.GridFS(db, collection="files")
# upload_file(file_loc=file_loc, file_name=file_name, fs=fs)
# download_file(download_loc=down_loc, db=db, fs=fs, file_name=file_name)