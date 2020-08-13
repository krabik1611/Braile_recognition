package com.lab104.translatebraill;

import android.content.Intent;
import android.content.pm.PackageManager;
import android.os.Bundle;
import android.util.DisplayMetrics;
import android.util.Log;
import android.util.Rational;
import android.util.Size;
import android.view.TextureView;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.Toast;


import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;
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



import java.io.File;


public class MainActivity extends AppCompatActivity {
    private static final int REQUEST_CODE_PERMISSIONS = 100;
    private static String[] REQUEST_PERMISSIONS = new String[]{
            "android.permission.CAMERA",
            "android.permission.WRITE_EXTERNAL_STORAGE",
            "android.permission.READ_EXTERNAL_STORAGE",
            "android.permission.FLASHLIGHT"
    };
    TextureView textureView;
    public static ViewGroup.LayoutParams params, paramsFrame;
    Toolbar tbTop, tbBottom;
    ConstraintLayout constraintLayout;
    ConstraintSet set;
    DisplayMetrics dm = new DisplayMetrics();
    public static File file;
    public static ImageView frame;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        getSupportActionBar().hide();
        Init();
    }

    private void Init()
    {
        tbTop = findViewById(R.id.toolbarTop);
        tbBottom = findViewById(R.id.toolbarBottom);
        textureView = findViewById(R.id.textureView);
        frame = findViewById(R.id.frame);
        paramsFrame = frame.getLayoutParams();
        params = textureView.getLayoutParams();
        getWindowManager().getDefaultDisplay().getMetrics(dm);
        params.width = dm.widthPixels;
        params.height = (dm.widthPixels*16)/9;
        Toast.makeText(this, Integer.toString(dm.heightPixels), Toast.LENGTH_SHORT).show();
        textureView.setLayoutParams(params);
        paramsFrame.height = (dm.heightPixels - (tbTop.getLayoutParams().height + tbBottom.getLayoutParams().height)) * 80 / 100;
        frame.setLayoutParams(paramsFrame);
        if (PermissionGranted())
        {
            StartCamera();
        }
        else
        {
            ActivityCompat.requestPermissions(this,REQUEST_PERMISSIONS,REQUEST_CODE_PERMISSIONS);
        }
    }

    private void StartCamera()
    {
        CameraX.unbindAll();
        Rational ratio = new Rational(textureView.getWidth(),textureView.getHeight());
        Size screen = new Size(dm.widthPixels,dm.heightPixels);

        PreviewConfig previewConfig = new PreviewConfig.Builder().setTargetAspectRatio(ratio).setTargetResolution(screen).build();
        Preview preview = new Preview(previewConfig);
        preview.setOnPreviewOutputUpdateListener(
                new Preview.OnPreviewOutputUpdateListener() {
                    @Override
                    public void onUpdated(Preview.PreviewOutput output) {
                        ViewGroup parent = (ViewGroup) textureView.getParent();
                        parent.removeView(textureView);
                        parent.addView(textureView,0);
                        textureView.setSurfaceTexture(output.getSurfaceTexture());



                    }
                }
        );
        ImageCaptureConfig imageCaptureConfig = new ImageCaptureConfig.Builder().
                setCaptureMode(ImageCapture.CaptureMode.MAX_QUALITY).build();
        final ImageCapture imageCapture = new ImageCapture(imageCaptureConfig);
        imageCapture.setFlashMode(FlashMode.ON);
        findViewById(R.id.fab).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                final File filedirs = new File(getFilesDir() + "/TranslateBraille/");
                filedirs.mkdirs();
                file = new File(filedirs, "photo.jpg");
                //Toast.makeText(MainActivity.this, file.getAbsolutePath(), Toast.LENGTH_SHORT).show();
                imageCapture.takePicture(file, new ImageCapture.OnImageSavedListener() {
                    @Override
                    public void onImageSaved(@NonNull File file) {
                        String msg = "Picture saved at " + file.getAbsolutePath();
                        Toast.makeText(MainActivity.this, msg, Toast.LENGTH_SHORT).show();
                        Log.d("path", msg);
                        GalleryActivity();
                    }

                    @Override
                    public void onError(@NonNull ImageCapture.UseCaseError useCaseError, @NonNull String message, @Nullable Throwable cause) {
                        String msg = "Picture was not captured: " + message;
                        Toast.makeText(MainActivity.this, msg, Toast.LENGTH_SHORT).show();
                        if (cause != null)
                        {
                            cause.printStackTrace();
                        }
                    }
                });
            }
        });
        CameraX.bindToLifecycle(this, preview, imageCapture);
        findViewById(R.id.fabmenu).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                /*setContentView(R.layout.activity_menu);
                findViewById(R.id.button).setOnClickListener(new View.OnClickListener() {
                    @Override
                    public void onClick(View view) {
                        Init();
                        StartCamera();
                    }
                });*/
            }
        });

    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if (requestCode == REQUEST_CODE_PERMISSIONS && PermissionGranted())
        {
            StartCamera();
        }
        else
        {
            Toast.makeText(this, "Permission was denied by the user!", Toast.LENGTH_SHORT).show();
            finish();
        }
    }

    private boolean PermissionGranted() {
        for (String permission : REQUEST_PERMISSIONS)
        {
            if (ContextCompat.checkSelfPermission(this,permission) != PackageManager.PERMISSION_GRANTED)
            {
                return false;
            }
        }
        return true;
    }

    public void GalleryActivity()
    {
        Intent intent = new Intent(this, GalleryActivity.class);
        startActivity(intent);

    }

}