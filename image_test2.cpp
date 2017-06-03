
#include <opencv2/highgui/highgui.hpp>
#include <cv_bridge/cv_bridge.h>
#include <time.h>
#include <sstream> // for converting the command line parameter to integer
#include "std_msgs/Int16MultiArray.h"
#include <stdint.h>

/*#include <pcl/point_types.h>
#include <pcl_ros/point_cloud.h>*/

using namespace std;
using namespace cv;

#define SIZE 262144

// Tuning parameters loaded from YAML file (file specified in launch file)
  int cannyThresh = 30;
  int ratio =3;
  int houghThreshold = 80;
  int houghMinLineLength = 30;
  int houghMaxLineGap = 5;
  int maxDistance = 8;
  int outputLineSpacing = 5;

int main(int argc, char** argv)
{
  std::vector<int> points;
  Mat src, thresh, mixed_src, canny, dst, cdst, blueOnly, src2, doneFrame; 
   cv::Mat src_img, working, fin_img;

  src = imread(argv[1], CV_LOAD_IMAGE_COLOR);
  namedWindow( "Preview", WINDOW_AUTOSIZE );// Create a window for display.
  imshow("Preview", src);

  src_img = src;

 // Convert image to grayscale
  cv::cvtColor(src_img, src_img, CV_BGR2GRAY);

  // Crops the image (removes sky)
  int topCrop = 2 * src_img.rows / 3;
  cv::Rect roiNoSky(0, topCrop, src_img.cols, src_img.rows - topCrop);
  src_img = src_img(roiNoSky);

  // Create blank canvas
  fin_img = cv::Mat::zeros(src_img.size(), src_img.type());

  // Gaussian Blur
  cv::GaussianBlur(src_img, working, cv::Size(3, 3), 2.0);

  // Detect edges
  cv::Canny(working, working, cannyThresh, cannyThresh*ratio, 3);

  // Erosion and dilation
  int kernel_size = 3;
  cv::Mat erosion_kernal = cv::getStructuringElement(cv::MORPH_CROSS, cv::Size(kernel_size, kernel_size));
  cv::dilate(working, working, erosion_kernal);
  cv::dilate(working, working, erosion_kernal);
  cv::dilate(working, working, erosion_kernal);
  cv::erode(working, working, erosion_kernal);
  cv::erode(working, working, erosion_kernal);
  cv::erode(working, working, erosion_kernal);

  // Find lines
  std::vector<cv::Vec4i> lines;
  cv::HoughLinesP(working, lines, 1.0, CV_PI / 180, houghThreshold, houghMinLineLength, houghMaxLineGap);
  for (size_t i = 0; i < lines.size(); ++i)
  {
    cv::LineIterator it(fin_img, cv::Point(lines[i][0], lines[i][1]), cv::Point(lines[i][2], lines[i][3]), 8);
    for (int j = 0; j < it.count; ++j, ++it)
    {
      if (j % outputLineSpacing == 0)
        fin_img.at<uchar>(it.pos()) = 255;
    }
  }
  

  // Re-fill sky area of image with black
  cv::Mat black = cv::Mat::zeros(cv::Size(src_img.cols, topCrop), src_img.type());
  cv::vconcat(black, fin_img, fin_img);
  imshow("final image", fin_img);   
  waitKey(0); 
  /*pcl::PointCloud<pcl::PointXYZ>::Ptr cloud;

  cloud = toPointCloud(tf_listener, MatToContours(fin_img), cam, topic);

  // Limit how far the points are plotted in the cloud
  capPointCloud(cloud, maxDistance);


  cv::cvtColor(fin_img, fin_img, CV_GRAY2BGR);*/
}


