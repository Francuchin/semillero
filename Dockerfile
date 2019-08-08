FROM spmallick/opencv-docker:opencv
WORKDIR /app
RUN pip3 install numpy scikit-image
COPY python/ /app
EXPOSE 8080

