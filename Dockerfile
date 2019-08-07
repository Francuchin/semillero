FROM spmallick/opencv-docker:opencv
WORKDIR /app
RUN pip3 install numpy scikit-image
COPY otsu/ /app
EXPOSE 8080

