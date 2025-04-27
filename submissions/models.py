from django.db import models

class UserSubmission(models.Model):
    vercel_blob_url = models.URLField(max_length=500, blank=False)  # To store the Vercel Blob URL
    email = models.EmailField(max_length=254, blank=False)  # To store the email ID
    x_post_url = models.URLField(max_length=500, blank=True, null=True)  # To store the X post URL (formerly Twitter)

    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the submission was made

    class Meta:
        verbose_name = "User Submission"
        verbose_name_plural = "User Submissions"
        ordering = ['-created_at']

    def __str__(self):
        return f"Submission by {self.email} on {self.created_at}"
