package com.lab104.translatebraill;

import androidx.appcompat.app.AppCompatActivity;
import androidx.constraintlayout.widget.ConstraintLayout;

import android.content.Context;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.Bitmap.Config;
import android.graphics.Matrix;
import android.graphics.drawable.BitmapDrawable;
import android.graphics.drawable.ClipDrawable;
import android.graphics.drawable.Drawable;
import android.media.Image;
import android.net.Uri;
import android.os.Bundle;
import android.text.Layout;
import android.util.DisplayMetrics;
import android.util.Log;
import android.view.View;
import android.view.ViewGroup;
import android.view.ViewGroup.LayoutParams;
import android.widget.ImageView;
import android.widget.Toast;

import java.io.File;

public class GalleryActivity extends AppCompatActivity {
    ImageView imageView, frame;
    LayoutParams params;
    DisplayMetrics displayMetrics = new DisplayMetrics();


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_gallery);
        Init();

    }

    private void Init() {
        imageView = findViewById(R.id.imageCrop);
        getWindowManager().getDefaultDisplay().getMetrics(displayMetrics);
        params = imageView.getLayoutParams();
        params.width = displayMetrics.widthPixels;
        params.height = (displayMetrics.widthPixels*16)/9;
        imageView.setLayoutParams(params);
        //imageView.setLayoutParams(CameraActivity.params);
        Bundle extras = getIntent().getExtras();
        Uri imageUri = null;

        if (extras != null) {
            imageUri = (Uri) extras.get("imageUri");
            imageView.setImageURI(imageUri);
        }

        Bitmap bitmap = ((BitmapDrawable) imageView.getDrawable()).getBitmap();



        int width =(int) (bitmap.getHeight()*9/16);
        int height =(int) (width*Math.sqrt(2));
        int x = (bitmap.getWidth() - width)/2;
        int y =(int) ((bitmap.getHeight() - height)/3f);
        Log.i("logging1",width + " - ширина " + height + " - высота");
//        Bitmap scaledBitmap = Bitmap.createScaledBitmap(bitmap, params.width, (params.width*4/3), true);
//        Log.d("debugURI",scaledBitmap.getWidth() + " - ширина" + scaledBitmap.getHeight() + " - высота");
//        imageView.setImageBitmap(scaledBitmap);
        //imageView.setLayoutParams(params);
        //imageView.setScaleType(ImageView.ScaleType.CENTER_CROP);
        Log.i("loging", String.format("Total memory = %s",
                (int) (Runtime.getRuntime().totalMemory() / 1024)));

        Bitmap bitmapClip = bitmap.createBitmap(width, height, Config.ARGB_8888);
        int[] pixels = new int[width * height];
        bitmap.getPixels(pixels,0,width,x,y,width,height);
        bitmapClip.setPixels(pixels,0,width,0,0,width,height);
        imageView.setImageBitmap(bitmapClip);
//        Log.d("debugBITMAP",bitmapClip.getWidth() + " - ширина" + bitmapClip.getHeight() + " - высота");
//        Bitmap bitmap =  ((BitmapDrawable) imageView.getDrawable()).getBitmap();
//        int pixelsclipHeight = CameraActivity.params.height - CameraActivity.paramsFrame.height;
 //       int pixelsclipWidth = CameraActivity.params.height - CameraActivity.paramsFrame.width;
  //      Matrix m = new Matrix();
   //     m.setTranslate(300, 200);
    //    Bitmap bitmapClip = bitmap.createBitmap(bitmap, 0, 0, pixelsclipWidth, pixelsclipHeight, m, true);
    //    int[] pixels = new int[1000 * 1000];
    //    bitmap.getPixels(pixels,5,5,0,0,5,5);
   //     bitmapClip.setPixels(pixels,5,5,0,0,5,5);
   //     imageView.setImageBitmap(bitmapClip);
   //     params = new ConstraintLayout.LayoutParams(ConstraintLayout.LayoutParams.MATCH_PARENT, ConstraintLayout.LayoutParams.MATCH_PARENT);
   //     imageView.setLayoutParams(params);
    //    imageView.setScaleType(ImageView.ScaleType.FIT_CENTER);
       /* params = imageView.getLayoutParams();
        params.height = MainActivity.paramsFrame.height;
        params.width = MainActivity.paramsFrame.width;
        imageView.setLayoutParams(params);*/

       // paramsFrame = frame.getLayoutParams();
        //imageView.setLayoutParams(paramsFrame);
    }
}