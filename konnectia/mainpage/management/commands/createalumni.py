from django.core.management.base import BaseCommand
from mainpage.models import User, Post

class Command(BaseCommand):
    help = 'Create sample alumni users and posts.'

    def handle(self, *args, **kwargs):
        sample_users = [
            {
                'username': 'john_doe',
                'first_name': 'John',
                'last_name': 'Doe',
                'content': 'Excited to share that I\'ve joined Google as a Senior Software Engineer! DSATM gave me the foundation I needed. #DSATMAlumni #TechCareer',
                'profile_pic': 'profile_pic/alumni1.jpg',
                'bio': 'Software Engineer @ Google | DSATM Alumni 2020'
            },
            {
                'username': 'sarah_smith',
                'first_name': 'Sarah',
                'last_name': 'Smith',
                'content': 'Just completed my Master\'s in Data Science from Stanford! Thank you DSATM for the amazing journey. #DSATMPride #DataScience',
                'profile_pic': 'profile_pic/alumni2.jpg',
                'bio': 'Data Scientist | Stanford Graduate | DSATM Alumni 2019'
            },
            {
                'username': 'mike_wilson',
                'first_name': 'Mike',
                'last_name': 'Wilson',
                'content': 'Started my own tech startup! The entrepreneurial spirit I developed at DSATM has been invaluable. #DSATMInnovation #StartupLife',
                'profile_pic': 'profile_pic/alumni3.jpg',
                'bio': 'Founder & CEO @ TechStart | DSATM Alumni 2018'
            },
            {
                'username': 'emma_chen',
                'first_name': 'Emma',
                'last_name': 'Chen',
                'content': 'Back on campus for the annual tech symposium! Great to see how DSATM has grown. #DSATMHomecoming #TechCommunity',
                'profile_pic': 'profile_pic/alumni4.jpg',
                'bio': 'Product Manager @ Microsoft | DSATM Alumni 2021'
            },
            {
                'username': 'alex_kumar',
                'first_name': 'Alex',
                'last_name': 'Kumar',
                'content': 'Just published my research paper on AI in healthcare! Thanks to my professors at DSATM for the guidance. #DSATMResearch #AIHealthcare',
                'profile_pic': 'profile_pic/alumni5.jpg',
                'bio': 'AI Researcher | PhD Candidate | DSATM Alumni 2020'
            }
        ]
        created_count = 0
        for user_data in sample_users:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                    'profile_pic': user_data['profile_pic'],
                    'bio': user_data['bio'],
                    'is_active': True
                }
            )
            if created:
                Post.objects.create(
                    creater=user,
                    content_text=user_data['content']
                )
                Post.objects.create(
                    creater=user,
                    content_text=f"Remembering my time at DSATM - the late night coding sessions, the hackathons, and the amazing friends I made. #DSATMMemories #CollegeLife"
                )
                created_count += 1
        self.stdout.write(self.style.SUCCESS(f'Created {created_count} alumni users and posts.')) 