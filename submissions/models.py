from django.db import models
class UserSubmission(models.Model):
    vercel_blob_url = models.URLField(max_length=500, blank=False)
    email = models.EmailField(max_length=254, blank=False)
    x_post_url = models.URLField(max_length=500, blank=True, null=True)
    memeforge_user = models.ForeignKey("users.MemeforgeUser", on_delete=models.CASCADE, null=True, related_name="submissions")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "User Submission"
        verbose_name_plural = "User Submissions"
        ordering = ['-created_at']

    def __str__(self):
        return f"Submission by {self.email} on {self.created_at}"
