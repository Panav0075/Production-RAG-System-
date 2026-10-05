Title: File Uploads
URL: https://docs.example.local/file-uploads

# File Uploads

Files can be uploaded through the web application or upload API. The maximum individual file size is 25 MB on Free, 250 MB on Pro, and 2 GB on Enterprise.

The upload API supports multipart uploads for files larger than 50 MB. Multipart sessions expire after 24 hours if they are not completed.

Executable file types are rejected. Uploaded files are scanned before they become available for download. A file that fails scanning is quarantined and is not exposed to workspace members.

Applications should calculate a checksum before multipart upload so the completed object can be verified.
