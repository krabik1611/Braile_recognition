package com.lab104.translatebraill;


import android.content.Context;
import android.os.Environment;
import android.util.Log;
import android.view.View;
import android.widget.Toast;

import androidx.annotation.NonNull;

import org.opencv.core.Core;
import org.opencv.core.CvType;
import org.opencv.core.Mat;
import org.opencv.core.MatOfPoint;
import org.opencv.core.MatOfPoint2f;
import org.opencv.core.Point;
import org.opencv.core.Rect;
import org.opencv.core.RotatedRect;
import org.opencv.core.Scalar;
import org.opencv.core.Size;
import org.opencv.imgcodecs.Imgcodecs;
import org.opencv.imgproc.Imgproc;

import java.io.File;
import java.lang.reflect.Array;
import java.util.ArrayList;
import java.util.List;

import static java.lang.Math.round;
import static java.lang.Math.sqrt;
import static org.opencv.imgproc.Imgproc.CHAIN_APPROX_SIMPLE;
import static org.opencv.imgproc.Imgproc.COLOR_BGR2GRAY;
import static org.opencv.imgproc.Imgproc.Canny;
import static org.opencv.imgproc.Imgproc.GaussianBlur;
import static org.opencv.imgproc.Imgproc.MORPH_CLOSE;
import static org.opencv.imgproc.Imgproc.MORPH_OPEN;
import static org.opencv.imgproc.Imgproc.MORPH_RECT;
import static org.opencv.imgproc.Imgproc.RETR_EXTERNAL;
import static org.opencv.imgproc.Imgproc.RETR_TREE;
import static org.opencv.imgproc.Imgproc.cvtColor;
import static org.opencv.imgproc.Imgproc.dilate;
import static org.opencv.imgproc.Imgproc.getGaborKernel;
import static org.opencv.imgproc.Imgproc.getRotationMatrix2D;
import static org.opencv.imgproc.Imgproc.warpAffine;


public class FindSymbol {

    public Mat Image;
    final File file = new File(Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_PICTURES)+"/TranslateBraille/Test.jpg");
    final File file1 = new File(Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_PICTURES)+"/TranslateBraille/");
    public int x;
    public int y;
    public Mat img;// = new Mat(new Size(1920, 1080), CvType.CV_8U);
    public Mat __dark__;
    public Mat __defaultKernel__;
    public Mat __DarkContours__;

    private Mat KERNEL = new Mat(new Size(5, 30), CvType.CV_8UC1, new Scalar(255));

    public void init(Context context) {
        Image = Imgcodecs.imread(file.getAbsolutePath());
        y = Image.width();
        x = Image.height();
        img = new Mat(new Size(x, y), CvType.CV_8U);

       //String msg = "Hello Yeah " + x +" "+ y;
        //Toast.makeText(context, msg, Toast.LENGTH_LONG).show();

        Mat __dark__ = new Mat(new Size(x,y), CvType.CV_32SC1);
        Mat __defaultKernel__ = Imgproc.getStructuringElement(MORPH_RECT,new Size(5,5));
        Imgproc.cvtColor(Image, img, COLOR_BGR2GRAY);

        Mat imgg = imgModify(img,"edges", new Mat(new Size(5,30),CvType.CV_8U));
        List<MatOfPoint> contoursRaw = findContour(imgg,"tree");
        List<MatOfPoint> contoursClear = delCont(contoursRaw);
        Log.d("Debug: ", "contoursClear");
        List<Mat> lines = cutWithMask(contoursClear);

        List<Mat> AllSymb = new ArrayList<>();

        for(int i=0;i<lines.size();i++){
            List<Mat> line = getSymbol(lines.get(i));
            AllSymb.addAll(line);
            for(int j=0;j<line.size();j++)
                Imgcodecs.imwrite(file1.getAbsolutePath()+"/"+i+"_"+j+".jpg",line.get(j));
        }

        //String msg ="fff"+ contoursClear;
        //Toast.makeText(context, msg, Toast.LENGTH_LONG).show();
        Log.d("Debug: ", "Seccessfull");
    };

    public Mat imgModify(Mat img,String key, Mat Kernel) {

        Mat img_1 = new Mat();
        Mat img_2 = new Mat();
        Mat edges = new Mat();

        Imgproc.GaussianBlur(img, img, new Size(5, 5), 0, 0);
        Imgproc.Canny(img, edges, 20, 70);
        Imgproc.dilate(edges, img_1, Kernel, new Point(-1,-1), 1);

        switch (key) {
            case "edges":
                return edges;
            case "dilate":
                return img_1;
            case "open":
                Imgproc.morphologyEx(img_1, img_2, MORPH_CLOSE, Kernel, new Point(-1,-1), 2);
                Imgproc.morphologyEx(img_2, img_2, MORPH_OPEN, Kernel, new Point(-1,-1), 2);
                break;
        }
        return img_2;
    };

    public List<MatOfPoint> findContour(Mat img,String key) {
        Mat hierarchy = new Mat();
        List<MatOfPoint> contours = new ArrayList<MatOfPoint>();
        switch (key) {
            case "external":
                Imgproc.findContours(img, contours, hierarchy, RETR_EXTERNAL, CHAIN_APPROX_SIMPLE);
                break;
            case "tree":
                Imgproc.findContours(img, contours, hierarchy, RETR_TREE, CHAIN_APPROX_SIMPLE);
        }
        return contours;
    }

    public List<MatOfPoint> delCont(List<MatOfPoint> contours){
        int[] LenLines = new int[contours.toArray().length];
        int count = 0;
        MatOfPoint temp;
        for(int i=0;i<contours.toArray().length;i++){
            temp = (MatOfPoint) contours.toArray()[i];
            LenLines[i] = temp.height();
            count += temp.height();
        }
        float mean = count / contours.size();
        double deviations = sqrt((count - mean) * (count - mean) / (contours.toArray().length-1));

        int j = 0;
        while (j < contours.size()){
            if (LenLines[j] > mean+deviations) contours.remove(j) ; else j++;
        }

        return contours;
    };

    public List<Mat> __findRect__(Mat img){
        List<MatOfPoint> cont = (List<MatOfPoint>) findContour(img,"tree");
        List<Mat> line = new ArrayList<>();
        MatOfPoint2f NewMtx;
        MatOfPoint temp;
        RotatedRect rect;
        Mat box = new Mat();
        Rect[] boxes = new Rect[cont.size()];
        for(int i=0;i<cont.size();i++){
            temp = (MatOfPoint) cont.toArray()[i];
            NewMtx = new MatOfPoint2f(temp.toArray());
            rect = Imgproc.minAreaRect(NewMtx);
            Imgproc.boxPoints(rect, box);
            boxes[i] = Imgproc.boundingRect(box);
           // Log.d("Debug1",boxes[i].toString());
        }
        Rect temp1;
        for(int i = 0;i<cont.size();i++){
            for(int j = 0;j<cont.size()-i-1;j++){
                if(boxes[i].y > boxes[i+1].y){
                    temp1 = boxes[i];
                    boxes[i] = boxes[i+1];
                    boxes[i+1] = temp1;
                }
            }
        }

        for(int i=0;i<cont.size();i++){
            if(boxes[i].x <0) boxes[i].x = 0;
            if(boxes[i].y <0) boxes[i].y = 0;
            //Mat imgage = img(boxes[i]);
            line.add(new Mat(img,boxes[i]));
            //Log.d("Debug1",boxes[i].toString()+"  "+ line.get(i));
            //Imgcodecs.imwrite(file1.getAbsolutePath()+"/"+i+".jpg", line.get(i));
        }
        return line;
    }
    public List<Mat> cutWithMask(List<MatOfPoint> contours){
        //Mat dark = __dark__;
        Mat dark = new Mat(Image.size(), Image.type());
        Imgproc.cvtColor(dark, dark, Imgproc.COLOR_RGBA2GRAY);
        Imgproc.drawContours(dark,contours,-1, new Scalar(255,255,255),1);
        Log.d("Debug1",dark.toString());
        __DarkContours__ = dark;

        Mat kernel = Imgproc.getStructuringElement(Imgproc.CV_SHAPE_RECT,new Size(5,5));
        Imgproc.morphologyEx(dark,dark,MORPH_CLOSE,kernel);

        int y;
        Mat mask = new Mat();
        Mat horizontalMask = imgModify(dark,"dilate", new Mat(new Size(5,this.x + this.x/2),CvType.CV_8U));
        Mat verticalMask = imgModify(dark,"dilate", new Mat(new Size(this.y,15),CvType.CV_8U));
        Core.bitwise_and(horizontalMask,verticalMask,mask);


        List<Mat> lines = __findRect__(mask);
        //lines = __rotationsLines__(lines);

        Log.d("Debug1","OK");
        for(int i=0;i< lines.size();i++){
            y = lines.get(i).width();
            Log.d("Debug1",""+lines.get(i));
            if (y>70){
                lines.addAll(i,checkString(lines.get(i)));
            }
        }
        Log.d("Debug1","OK");
        return lines;
    }

    private double checkAngle(Mat img){
        Mat lines = new Mat();
        Imgproc.HoughLines(img,lines,1,Math.PI/180,250);
        double mean = 0;

        for(int i=0;i < lines.rows();i++){
            double rho = lines.get(i,0)[0],
                    theta = lines.get(i,0)[1];
            double a = Math.cos(theta);
            mean += a;
        }
        mean = mean / lines.rows();
        return Math.toDegrees(mean);
    }

    public List<Mat> __rotationsLines__(@NonNull List<Mat> lines){
        List<Mat> line = new ArrayList<>();
        Mat kernel = Imgproc.getStructuringElement(Imgproc.CV_SHAPE_RECT,new Size(5,5));
        Mat kernel_dilate = Imgproc.getStructuringElement(Imgproc.CV_SHAPE_RECT,new Size(1,50));

        for(int i=0;i < lines.size();i++){
            int x = lines.get(i).height();
            int y = lines.get(i).width();

            Mat linet = new Mat();
            Mat edges = new Mat();
            Mat test = new Mat();
            double grad;

            Imgproc.GaussianBlur(lines.get(i),linet,new Size(5,5),0);
            Mat kernel_imgModigy = Imgproc.getStructuringElement(Imgproc.CV_SHAPE_RECT,new Size(5,30));
            edges = imgModify(linet,"edges",kernel_imgModigy);
            Imgproc.morphologyEx(edges,edges,MORPH_CLOSE,kernel);
            Imgproc.dilate(edges,edges,kernel_dilate,new Point(-1,-1),2);
            grad = checkAngle(edges);
            Mat M = getRotationMatrix2D(new Point(x,y),grad,1.0);
            warpAffine(lines.get(i),test, M, new Size(x,y));
            line.add(test);
        }
        return line;
    }

    public List<Mat> checkString(Mat img){
        int x = img.height();
        int y = img.width();
        Mat edges = new Mat();
        Mat kernel = Imgproc.getStructuringElement(Imgproc.CV_SHAPE_RECT,new Size(1,x*1.5));
        Mat image = __DarkContours__;
        Mat linel = new Mat();

        Imgproc.Canny(img, edges, 30, 70);
        List<MatOfPoint> cont = findContour(edges,"tree");
        cont = delCont(cont);
        dilate(image,linel,kernel,new Point(-1,-1),1);
        List<MatOfPoint> controus = findContour(linel,"tree");

        List<Mat> line = new ArrayList<>();
        MatOfPoint2f NewMtx;
        MatOfPoint temp;
        RotatedRect rect;
        Mat box = new Mat();
        Rect[] boxes = new Rect[controus.size()];
        Log.d("Debug1","OK_checkstring");
        for(int i=0;i<controus.size();i++){
            temp = (MatOfPoint) cont.toArray()[i];
            NewMtx = new MatOfPoint2f(temp.toArray());
            rect = Imgproc.minAreaRect(NewMtx);
            Imgproc.boxPoints(rect, box);
            Rect a = Imgproc.boundingRect(box);
            a = new Rect(0,a.y, a.width,a.height);
            line.add(new Mat(img, a));
        }
        return line;
    }
    public List<Mat> getSymbol(Mat line){
        List<Mat> symbImg = new ArrayList<>();
        List<float[]> symbol = new ArrayList<>();
        int x = line.height();
        int y = line.width();
        Mat edges = new Mat();
        Mat kernel = new Mat(new Size(y,3), CvType.CV_8S);

        Imgproc.Canny(line, edges, 30, 70);
        Imgproc.morphologyEx(edges,edges,MORPH_CLOSE,kernel);

        List<MatOfPoint> controus = findContour(edges,"tree");

        float SredX = 0;
        MatOfPoint2f NewMtx;
        MatOfPoint temp;
        RotatedRect rect;
        Mat box = new Mat();

        for(int j=0;j<2;j++){
            for(int i=0;i<controus.size();i++){
                temp = (MatOfPoint) controus.toArray()[i];
                NewMtx = new MatOfPoint2f(temp.toArray());
                rect = Imgproc.minAreaRect(NewMtx);
                Imgproc.boxPoints(rect, box);
                Rect a = Imgproc.boundingRect(box);
                if (i == 0){
                    SredX += (a.x+a.width) / controus.size();
                }else{
                    if((a.x+a.width)/SredX > 1.5){
                        float[] temp_2 =  {a.x,(a.x+a.width)/2+a.x+3};
                        symbol.add(temp_2);
                        temp_2 = new float[]{a.x + (a.x + a.width) / 2 - 3, a.x + a.width + a.x + 3};
                        symbol.add(temp_2);
                    }else if((a.x+a.width)/SredX < 0.7){
                        float[] temp_2 =  {a.x-3,SredX+a.x+3};
                        symbol.add(temp_2);
                    }else {
                        float[] temp_2 = {a.x-3, (a.x + a.width) + a.x + 3};
                        symbol.add(temp_2);
                    }
                }
            }
        }

        List<float[]> space = new ArrayList<>();
        List<Integer> test = new ArrayList<>();

        int SredX_ = Math.round(SredX);
        for(int i=1;i<symbol.size();i++){
            if(symbol.get(i)[0] - symbol.get(i-1)[1] > SredX){
                space.add(new float[]{symbol.get(i-1)[1],symbol.get(i-1)[1]+SredX});
                test.add(i);
            }
        }
        for(int i=0;i<test.size();i++)
            symbol.add(test.get(i)+i,space.get(i));

        for(int i=0;i<symbol.size();i++){
            if(Math.round(symbol.get(i)[0]) < 0) symbol.get(i)[0] = 0;
            if(Math.round(symbol.get(i)[1]) < 0) symbol.get(i)[1] = 0;
            Rect rected = new Rect(0, y, Math.round(symbol.get(i)[0]),Math.round(symbol.get(i)[1]));
            symbImg.add(new Mat(line,rected));
        }
        return symbImg;
    }

}