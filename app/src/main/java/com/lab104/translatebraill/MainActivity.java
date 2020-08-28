package com.lab104.translatebraill;

import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.pm.ActivityInfo;
import android.content.pm.PackageManager;
import android.database.Cursor;
import android.graphics.Matrix;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorEventListener2;
import android.hardware.SensorManager;
import android.net.Uri;
import android.opengl.GLSurfaceView;
import android.opengl.GLSurfaceView.Renderer;
import android.os.Bundle;
import android.util.DisplayMetrics;
import android.util.Log;
import android.util.Rational;
import android.util.Size;
import android.view.Surface;
import android.view.SurfaceView;
import android.view.TextureView;
import android.view.View;
import android.view.ViewGroup;
import android.view.WindowManager;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.Toast;


import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.app.AppCompatDialogFragment;
import androidx.appcompat.widget.Toolbar;
import androidx.camera.core.CameraX;
import androidx.camera.core.FlashMode;
import androidx.camera.core.ImageCapture;
import androidx.camera.core.ImageCaptureConfig;
import androidx.camera.core.Preview;
import androidx.camera.core.PreviewConfig;
import androidx.constraintlayout.widget.ConstraintLayout;
import androidx.constraintlayout.widget.ConstraintSet;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;
import androidx.fragment.app.FragmentManager;


import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.nio.channels.FileChannel;
import java.util.Arrays;
import java.util.Timer;
import java.util.TimerTask;

import javax.microedition.khronos.egl.EGLConfig;
import javax.microedition.khronos.opengles.GL10;


public class MainActivity extends AppCompatActivity {
    public static final int START_ACTIVITY_GALLERY = 101;
    public Uri chosenImageUri;
    public ImageView imageView;
    Button btnToCamera, btnToUpload;
    ImageView background;
    SensorManager sensorManager;
    Sensor sensorLinAccel;
    float X = 0,X2;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);
        this.getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN, WindowManager.LayoutParams.FLAG_FULLSCREEN);
        background = findViewById(R.id.backgroundMain);
//        sensorManager = (SensorManager) getSystemService(SENSOR_SERVICE);
//        sensorLinAccel = sensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER);
        ButttonHandler();


    }

    private void ButttonHandler() {
        btnToCamera = findViewById(R.id.btnToCamera);
        btnToUpload = findViewById(R.id.btnToUpload);
        btnToCamera.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(getApplicationContext(),CameraActivity.class);
                startActivity(intent);
            }
        });
        btnToUpload.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(Intent.ACTION_GET_CONTENT);
                intent.setType("image/*");
                startActivityForResult(intent, 1);
            }

        });


    }
    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data)
    {
        super.onActivityResult(requestCode, resultCode, data);

        if (resultCode == RESULT_OK && requestCode == 1)
        {
            chosenImageUri = data.getData();
//            final int chunkSize = 1024;  // We'll read in one kB at a time
//            byte[] imageData = new byte[chunkSize];
//            try {
//                InputStream in = getContentResolver().openInputStream(chosenImageUri);
//                OutputStream out = new FileOutputStream(new File(getFilesDir() + "/TranslateBraille/" + "photo.jpg"));
//
//                int bytesRead;
//                while ((bytesRead = in.read(imageData)) > 0) {
//                    out.write(Arrays.copyOfRange(imageData, 0, Math.max(0, bytesRead)));
//                }
//                in.close();
//                out.close();
//            } catch (Exception ex) {
//            }
            Intent intent = new Intent(getApplicationContext(),CropActivity.class);
            intent.putExtra("imageUri",chosenImageUri);
            startActivity(intent);

        }
    }


//    @Override
//    protected void onResume() {
//        super.onResume();
//        sensorManager.registerListener(listener, sensorLinAccel,
//                SensorManager.SENSOR_DELAY_NORMAL);
//    }
//
//    @Override
//    protected void onPause() {
//        super.onPause();
//        sensorManager.unregisterListener(listener);
//    }
//
//
//    SensorEventListener listener = new SensorEventListener() {
//
//        @Override
//        public void onAccuracyChanged(Sensor sensor, int accuracy) {
//        }
//
//        @Override
//        public void onSensorChanged(SensorEvent event) {
//            if (event.sensor.getType() == Sensor.TYPE_ACCELEROMETER)
//            {
//                    X = 70*event.values[0];
//                    ChangeBackground();
//            }
//
//        }
//
//    };
//
//    private void ChangeBackground() {
//        Log.d("DebugX", String.valueOf(X));
//        if ((int)X!=0 && Math.abs(X)>100)
//            if (X>0)
//            {
//                for (int i=10;i<X;i+=1)
//                    background.setPadding((int)X2+i,0,0,0);
//            }
//        else
//            {
//                for (int i=(int)X2;i>X;i-=1)
//                    background.setPadding((int)X2+i,0,0,0);
//            }
//            X2=X;
//    }

}

