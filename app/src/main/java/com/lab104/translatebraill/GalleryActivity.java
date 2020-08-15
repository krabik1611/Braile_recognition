package com.lab104.translatebraill;

import androidx.appcompat.app.AppCompatActivity;
import androidx.constraintlayout.widget.ConstraintLayout;

import android.content.Context;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.Matrix;
import android.graphics.drawable.BitmapDrawable;
import android.graphics.drawable.Drawable;
import android.media.Image;
import android.net.Uri;
import android.os.Bundle;
import android.text.Layout;
import android.util.Log;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.Toast;

public class GalleryActivity extends AppCompatActivity {
    ImageView imageView, frame;
    ConstraintLayout.LayoutParams params, paramsFrame;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_gallery);
        Init();

    }

    private void Init() {
        imageView = findViewById(R.id.imageCrop);
        //imageView.setLayoutParams(CameraActivity.params);
        Bundle extras = getIntent().getExtras();
        Uri imageUri = null;

        if (extras != null) {
            imageUri = (Uri) extras.get("imageUri");
            imageView.setImageURI(imageUri);
        }

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