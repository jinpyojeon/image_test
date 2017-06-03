
#include <opencv2/highgui/highgui.hpp>
#include <cv_bridge/cv_bridge.h>
#include <time.h>
#include <sstream> // for converting the command line parameter to integer
#include "std_msgs/Int16MultiArray.h"
#include <stdint.h>

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

  cv_bridge::CvImagePtr cv_ptr;
  typedef pcl::PointCloud<pcl::PointXYZ> PCLCloud;


  Mat src_img = msg_img;

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
  pcl::PointCloud<pcl::PointXYZ>::Ptr cloud;

  cloud = toPointCloud(tf_listener, MatToContours(fin_img), cam, topic);

  // Limit how far the points are plotted in the cloud
  capPointCloud(cloud, maxDistance);


  cv::cvtColor(fin_img, fin_img, CV_GRAY2BGR);
}

LineDetector::LineDetector(ros::NodeHandle& handle, const std::string& topic)
  : _it(handle), topic(topic), tf_listener(handle)
{
  _src_img_info = _it.subscribeCamera(topic + "/image_raw", 1, &LineDetector::info_img_callback, this);
  _filt_img = _it.advertise(topic + "/filt_img", 1);
  _line_cloud = handle.advertise<PCLCloud>(topic + "/line_cloud", 100);

  handle.getParam(ros::this_node::getName() + "/config/line/cannyThresh", cannyThresh);
  handle.getParam(ros::this_node::getName() + "/config/line/ratio", ratio);
  handle.getParam(ros::this_node::getName() + "/config/line/houghThreshold", houghThreshold);
  handle.getParam(ros::this_node::getName() + "/config/line/houghMinLineLength", houghMinLineLength);
  handle.getParam(ros::this_node::getName() + "/config/line/houghMaxLineGap", houghMaxLineGap);
  handle.getParam(ros::this_node::getName() + "/config/line/maxDistance", maxDistance);
  handle.getParam(ros::this_node::getName() + "/config/line/outputLineSpacing", outputLineSpacing);
}
Contact GitHub API Training Shop Blog About
© 2017 GitHub, Inc. Terms Privacy Security Status Help