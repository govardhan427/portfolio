from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
import os
from django.views.decorators.cache import cache_page # <-- NEW IMPORT
from django.utils.decorators import method_decorator # <-- NEW IMPORT
from django.conf import settings
from mailjet_rest import Client
from rest_framework import status
from .models import Project, Skill, Certificate, Journey, Achievement
from .serializers import ProjectSerializer, SkillSerializer, CertificateSerializer, JourneySerializer, AchievementSerializer

class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows projects to be viewed.
    Lookups are done by 'slug' instead of 'id' for better SEO URLs.
    """
    queryset = Project.objects.all().order_by('-created_at')
    serializer_class = ProjectSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'

class SkillListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        skills = Skill.objects.all()
        serializer = SkillSerializer(skills, many=True)
        return Response(serializer.data)

@method_decorator(cache_page(settings.HOME_CACHE_TIMEOUT), name='get')
class HomeDataView(APIView):
    """
    The 'Masterpiece' Endpoint. 
    Fetches everything needed for the Homepage in 1 request.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        # 1. Featured Projects
        featured_projects = Project.objects.filter(featured=True).order_by('?')[:3] # Randomize or order by date
        
        # 2. Skills
        skills = Skill.objects.filter(is_featured=True) # Only show featured skills on home
        if not skills.exists():
            skills = Skill.objects.all()[:8] # Fallback to first 8 if none featured

        # 3. Certificates
        certs = Certificate.objects.all().order_by('-date_issued')

        # 4. Journey
        journey = Journey.objects.all().order_by('order')

        # 5. Achievements
        achievements = Achievement.objects.all().order_by('order')

        return Response({
            # The KEYS below must match exactly what React expects:
            'featured_projects': ProjectSerializer(featured_projects, many=True).data,
            'skills': SkillSerializer(skills, many=True).data,
            'certificates': CertificateSerializer(certs, many=True).data,
            'journey': JourneySerializer(journey, many=True).data,
            'achievements': AchievementSerializer(achievements, many=True).data,
            
            # Text Fields
            'hero_title': "Full-Stack Developer & DevOps Enthusiast",
            'about_text': "I build scalable web apps and automate their deployment."
        })
class ContactAPIView(APIView):
    """
    Sends an email using Mailjet when a user submits the contact form.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        name = request.data.get('name')
        email = request.data.get('email') # The visitor's email
        message = request.data.get('message')

        if not name or not email or not message:
            return Response({"error": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Initialize Mailjet
        api_key = os.getenv('MAILJET_API_KEY')
        api_secret = os.getenv('MAILJET_API_SECRET')
        sender_email = os.getenv('MAILJET_SENDER_EMAIL')
        receiver_email = os.getenv('MAILJET_RECEIVER_EMAIL')

        mailjet = Client(auth=(api_key, api_secret), version='v3.1')

        # Construct the email
        data = {
          'Messages': [
            {
              "From": {
                "Email": sender_email,
                "Name": "Portfolio Bot"
              },
              "To": [
                {
                  "Email": receiver_email,
                  "Name": "Govardhan"
                }
              ],
              "ReplyTo": {
                  "Email": email,
                  "Name": name
              },
              "Subject": f"New Contact: {name}",
              "TextPart": f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}",
              "HTMLPart": f"""
                <h3>New Message from Portfolio</h3>
                <p><b>Name:</b> {name}</p>
                <p><b>Email:</b> {email}</p>
                <br/>
                <p><b>Message:</b></p>
                <p>{message}</p>
              """
            }
          ]
        }

        try:
            result = mailjet.send.create(data=data)
            if result.status_code == 200:
                return Response({"status": "sent"})
            else:
                return Response({"error": "Failed to send email"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            print(f"Mailjet Error: {e}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)