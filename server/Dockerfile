#publicly available docker image "python" on docker hub will be pulled

FROM python

EXPOSE 50007

#copying server from local directory to container's  folder

COPY s.py /home/s.py
COPY britney.mp3 /home/britney.mp3


#set working dir
WORKDIR /home

#running s.py in container

CMD python /home/s.py