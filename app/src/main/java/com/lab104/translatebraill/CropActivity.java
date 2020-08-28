package com.lab104.translatebraill;

import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.app.AppCompatDialogFragment;
import androidx.core.content.ContextCompat;
import androidx.fragment.app.FragmentManager;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.util.Log;

import com.yalantis.ucrop.UCrop;
import com.yalantis.ucrop.UCropActivity;
import com.yalantis.ucrop.UCropFragment;
import com.yalantis.ucrop.UCropFragmentCallback;
import com.yalantis.ucrop.view.UCropView;

import java.io.File;

public class CropActivity extends AppCompatActivity implements UCropFragmentCallback {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        Init();
    }

    private void Init() {
        Uri imageUri = (Uri) getIntent().getParcelableExtra("imageUri");
        Uri destinationUri = Uri.fromFile(new File(getFilesDir() + "/TranslateBraille/" + "photo1.jpg"));
        UCrop.Options options = new UCrop.Options();
        UCrop uCrop = UCrop.of(imageUri,destinationUri);
        options.setCompressionQuality(100);
        options.setToolbarColor(ContextCompat.getColor(this, R.color.Мусульманский_зелёный));
        options.setStatusBarColor(ContextCompat.getColor(this, R.color.Мусульманский_зелёный));
        options.setActiveControlsWidgetColor(ContextCompat.getColor(this, R.color.Мусульманский_зелёный));
        options.withAspectRatio(1,(int) Math.sqrt(2));
        options.setFreeStyleCropEnabled(true);
        uCrop.withOptions(options);
        UCropFragment fragment = uCrop.getFragment(uCrop.getIntent(this).getExtras());
        getSupportFragmentManager().beginTransaction()
                .add(R.id.fragment_container, fragment, UCropFragment.TAG)
                .commitAllowingStateLoss();
        uCrop.start(CropActivity.this,fragment);
        new AlertDialog.Builder(fragment.getActivity())
                .setTitle("Delete entry")
                .setMessage("Are you sure you want to delete this entry?")
                .setPositiveButton(android.R.string.yes, new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface dialog, int which) {
                    }
                })
                .setNegativeButton(android.R.string.no, null)
                .setIcon(android.R.drawable.ic_dialog_alert)
                .show();
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        switch (requestCode) {
            case UCrop.REQUEST_CROP:
                if (resultCode == RESULT_OK) {


                    handleUCropResult(data);
                }
                else
                {
                    setResultCancelled();
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

    @Override
    public void loadingProgress(boolean showLoader) {

    }

    @Override
    public void onCropFinish(UCropFragment.UCropResult result) {

    }
}