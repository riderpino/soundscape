# soundscape

Building with docker: 

1 . install docker engine 

2. in the directory: docker build -t soundscape_app .
3. docker run -d \
  --restart unless-stopped \
  -p 8501:80 \
  -e BACKUP_DIR=/backup \
  -v /the_backupdirectory:/backup \
  --name soundscape \
  soundscape_app
