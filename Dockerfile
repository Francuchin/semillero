FROM spmallick/opencv-docker:opencv
WORKDIR /app
COPY otsu/ /app
CMD 'pip install numpy'
EXPOSE 8080

