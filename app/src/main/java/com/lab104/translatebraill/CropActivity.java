package com.lab104.translatebraill;

import androidx.annotation.ColorInt;
import androidx.annotation.DrawableRes;
import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.ActionBar;
import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.app.AppCompatDialogFragment;
import androidx.appcompat.app.WindowDecorActionBar;
import androidx.appcompat.widget.Toolbar;
import androidx.core.content.ContextCompat;
import androidx.fragment.app.FragmentManager;

import android.annotation.TargetApi;
import android.app.Activity;
import android.app.AlertDialog;
import android.app.AlertDialog.Builder;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.graphics.Color;
import android.graphics.PorterDuff;
import android.graphics.drawable.Animatable;
import android.graphics.drawable.Drawable;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.Window;
import android.view.WindowManager;
import android.widget.TextView;
import android.widget.Toast;

import com.yalantis.ucrop.UCrop;
import com.yalantis.ucrop.UCropActivity;
import com.yalantis.ucrop.UCropFragment;
import com.yalantis.ucrop.UCropFragmentCallback;
import com.yalantis.ucrop.view.UCropView;

import java.io.File;

public class CropActivity extends AppCompatActivity {

    UCropFragment fragment;
    UCrop uCrop;
    private boolean mShowLoader;

    Toolbar toolbar;
    private String mToolbarTitle;
    @DrawableRes
    private int mToolbarCancelDrawable;
    @DrawableRes
    private int mToolbarCropDrawable;
    // Enables dynamic coloring
    private int mToolbarColor;
    private int mStatusBarColor;
    private int mToolbarWidgetColor;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_crop);
        Init();
    }

    private void Init() {
        toolbar = findViewById(R.id.toolbar);
        Uri imageUri = (Uri) getIntent().getParcelableExtra("imageUri");
        Uri destinationUri = Uri.fromFile(new File(getFilesDir() + "/TranslateBraille/" + "photo1.jpg"));
        UCrop.Options options = new UCrop.Options();
        uCrop = UCrop.of(imageUri,destinationUri);
        options.setCompressionQuality(100);
        options.setToolbarColor(ContextCompat.getColor(this, R.color.Мусульманский_зелёный));
        options.setStatusBarColor(ContextCompat.getColor(this, R.color.Мусульманский_зелёный));
        options.setActiveControlsWidgetColor(ContextCompat.getColor(this, R.color.Мусульманский_зелёный));
        options.withAspectRatio(1,(int) Math.sqrt(2));
        options.setFreeStyleCropEnabled(true);
        uCrop.withOptions(options);
        uCrop.start(CropActivity.this);

    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        super.onActivityResult(requestCode, resultCode, data);

        if (requestCode == UCrop.REQUEST_CROP)
        {
            if (resultCode==RESULT_OK)
            {
                handleUCropResult(data);
            }
        }
    }

    private void handleUCropResult(Intent data) {
        if (data == null) {
            setResultCancelled();
            return;
        }
        final Uri resultUri = UCrop.getOutput(data);
        setResultOk(resultUri);
    }
    private void setResultOk(Uri imagePath) {
        Intent intent = new Intent();
        intent.putExtra("path", imagePath);
        setResult(Activity.RESULT_OK, intent);
        finish();
    }
    private void setResultCancelled() {
        Intent intent = new Intent();
        setResult(Activity.RESULT_CANCELED, intent);
        finish();
    }

}