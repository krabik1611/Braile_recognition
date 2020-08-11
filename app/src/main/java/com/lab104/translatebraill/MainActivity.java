package com.lab104.translatebraill;

import android.content.pm.PackageManager;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Color;
import android.graphics.drawable.Drawable;
import android.hardware.Camera;
import android.net.Uri;
import android.os.Bundle;
import android.os.Environment;
import android.os.SystemClock;
import android.sax.StartElementListener;
import android.text.Layout;
import android.util.DisplayMetrics;
import android.util.Rational;
import android.util.Size;
import android.view.TextureView;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.Switch;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.Toolbar;
import androidx.camera.core.CameraX;
import androidx.camera.core.ImageCapture;
import androidx.camera.core.ImageCaptureConfig;
import androidx.camera.core.Preview;
import androidx.camera.core.PreviewConfig;
import androidx.constraintlayout.widget.ConstraintLayout;
import androidx.constraintlayout.widget.ConstraintSet;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

import java.io.File;
import java.security.Policy;


public class MainActivity extends AppCompatActivity {
    private static final int REQUEST_CODE_PERMISSIONS = 100;
    private static String[] REQUEST_PERMISSIONS = new String[]{
            "android.permission.CAMERA",
            "android.permission.WRITE_EXTERNAL_STORAGE",
            "android.permission.READ_EXTERNAL_STORAGE",
            "android.permission.FLASHLIGHT"
    };
    TextureView textureView;
    ViewGroup.LayoutParams params, paramstool;
    Toolbar toolbar;
    ImageView imageView;
    ConstraintLayout constraintLayout;
    ConstraintSet set;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        Init();


        if (PermissionGranted())
        {
            StartCamera();
        }
        else
        {
            ActivityCompat.requestPermissions(this,REQUEST_PERMISSIONS,REQUEST_CODE_PERMISSIONS);
        }

    }

    private void Init()
    {
        setContentView(R.layout.activity_main);
        getSupportActionBar().hide();
        textureView = findViewById(R.id.textureView);
        params = textureView.getLayoutParams();
        DisplayMetrics dm = new DisplayMetrics();
        getWindowManager().getDefaultDisplay().getMetrics(dm);
        params.width = dm.widthPixels;
        params.height = (dm.widthPixels*16)/9;
        Toast.makeText(this, Integer.toString(dm.heightPixels), Toast.LENGTH_SHORT).show();
        textureView.setLayoutParams(params);
        toolbar = findViewById(R.id.toolbarTop);
        paramstool = toolbar.getLayoutParams();
        int heightTBtop = paramstool.height;
        toolbar = findViewById(R.id.toolbarBottom);
        paramstool = toolbar.getLayoutParams();
        paramstool.width = dm.widthPixels;
        //paramstool.height = dm.heightPixels - (params.height + heightTBtop);
        toolbar.setLayoutParams(paramstool);
        set = new ConstraintSet();
        constraintLayout = findViewById(R.id.layout);
        set.clone(constraintLayout);
        set.connect(R.id.frame, ConstraintSet.TOP, R.id.toolbarTop, ConstraintSet.BOTTOM);
        set.connect(R.id.frame, ConstraintSet.BOTTOM, R.id.toolbarBottom, ConstraintSet.TOP);
        set.applyTo(constraintLayout);
    }

    private void StartCamera()
    {
        CameraX.unbindAll();
        Rational ratio = new Rational(textureView.getHeight(),textureView.getWidth());
        Size screen = new Size(params.height,params.width);

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
                setCaptureMode(ImageCapture.CaptureMode.MIN_LATENCY).build();
        final ImageCapture imageCapture = new ImageCapture(imageCaptureConfig);


        findViewById(R.id.fab).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                final File filedirs = new File(getFilesDir() + "/TranslateBraille/");
                filedirs.mkdirs();
                File file = new File(filedirs, "photo.jpg");
                Toast.makeText(MainActivity.this, file.getAbsolutePath(), Toast.LENGTH_SHORT).show();
                imageCapture.takePicture(file, new ImageCapture.OnImageSavedListener() {
                    @Override
                    public void onImageSaved(@NonNull File file) {
                        String msg = "Picture saved at " + file.getAbsolutePath();
                        Toast.makeText(MainActivity.this, msg, Toast.LENGTH_SHORT).show();
                        setContentView(R.layout.galllery_main);
                        imageView = findViewById(R.id.imageView);
                        imageView.setImageURI(Uri.parse("file://" + file.getAbsolutePath()));

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
                setContentView(R.layout.menu_main);
                findViewById(R.id.button).setOnClickListener(new View.OnClickListener() {
                    @Override
                    public void onClick(View view) {
                        Init();
                        StartCamera();
                    }
                });
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
}