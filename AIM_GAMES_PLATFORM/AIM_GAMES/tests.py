from django.test import TestCase
from AIM_GAMES.models import *
from django.utils import timezone
# Create your tests here.

class AIM_GAMES_TestCase(TestCase):
    
    def test_tag(self):
        tag=Tag.objects.create(title="Tag 1")
        self.assertEqual(tag.title, 'Tag 1')

    def test_graphicEngine(self):
        ge=GraphicEngine.objects.create(title="GraphicEngine 1")
        self.assertEqual(ge.title, 'GraphicEngine 1')
    
    def test_url(self):
        url=URL.objects.create(id=20,uri="http://www.pruebas.com")
        self.assertEqual(url.id, 20)

    def test_Profile(self):
        user1 = User.objects.create_user(username='userProfileTest', password='userProfilePass')
        url1=URL.objects.create(uri="http://www.pruebas.com")
        profile1= Profile(id=56,user=user1, name='Antonio', surname='Arenas', email='antonio@test.com', city='Sevilla', 
            postalCode='41008', idCardNumber='12345678A', dateOfBirth='1990-12-12 00:00', phoneNumber='691000000',photo=url1)
        self.assertEqual(profile1.id, 56)
    
    def test_Freelancer(self):
        user2 = User.objects.create_user(username='userFreelancerTest', password='userFreelancerPass')
        url2=URL.objects.create(uri="http://www.pruebas.com")
        profile2= Profile(id=56,user=user2, name='AntonioF', surname='ArenasF', email='antoniof@test.com', city='Sevilla', 
            postalCode='41008', idCardNumber='12345678A', dateOfBirth='1990-12-12 00:00', phoneNumber='691000000',photo=url2)
        freelancer1= Freelancer.objects.create(id=90,profile=profile2,profession='Test profesion')
        self.assertEqual(freelancer1.id, 90)

    def test_Manager(self):
        user3 = User.objects.create_user(username='userBusinessTest', password='userBusinessPass')
        url3=URL.objects.create(uri="http://www.pruebas.com")
        profile3= Profile(user=user3, name='AntonioF', surname='ArenasF', email='antoniof@test.com', city='Sevilla', 
            postalCode='41008', idCardNumber='12345678A', dateOfBirth='1990-12-12 00:00', phoneNumber='691000000',photo=url3)
        manager1= Manager.objects.create(id=58,profile=profile3)
        self.assertEqual(manager1.id, 58)

    def test_Curriculum(self):
        user4 = User.objects.create_user(username='userCurriculumTest', password='userCurriculumPass')
        url4=URL.objects.create(uri="http://www.pruebasC.com")
        profile4= Profile(user=user4, name='AntonioC', surname='ArenasC', email='antonioc@test.com', city='Sevilla', 
            postalCode='41008', idCardNumber='12345678A', dateOfBirth='1990-12-12 00:00', phoneNumber='691000000',photo=url4)
        freelancer4= Freelancer.objects.create(profile=profile4,profession='Test curriculum')
        curriculum1= Curriculum.objects.create(id= 458,freelancer=freelancer4,verified=True)
        self.assertEqual(curriculum1.id, 458)

    def test_Profesional_Experience(self):
        user5 = User.objects.create_user(username='userPExperienceTest', password='userPExperiencePass')
        url5=URL.objects.create(uri="http://www.pruebasPE.com")
        profile5= Profile(user=user5, name='AntonioP', surname='ArenasE', email='antoniope@test.com', city='Sevilla', 
            postalCode='41008', idCardNumber='12345678A', dateOfBirth='1990-12-12 00:00', phoneNumber='691000000',photo=url5)
        freelancer5= Freelancer.objects.create(profile=profile5,profession='Test profesionalExperience')
        curriculum1= Curriculum.objects.create(freelancer=freelancer5,verified=True)
        professionalExperience1= ProfessionalExperience.objects.create(id= 78, curriculum=curriculum1, center='CentroPRueba', formation="FormacionPrueba",
        startDate="2017-01-13", endDate="2019-01-10", miniature="http://www.miniature.com")
        self.assertEqual(professionalExperience1.id, 78)

    def test_GraphicEngine_Experience(self):
        user5 = User.objects.create_user(username='userGEExperienceTest', password='userGEExperiencePass')
        url5=URL.objects.create(uri="http://www.pruebasGEE.com")
        profile5= Profile(user=user5, name='AntonioG', surname='ArenasEE', email='antonioGEE@test.com', city='Sevilla', 
            postalCode='41008', idCardNumber='12345678A', dateOfBirth='1990-12-12 00:00', phoneNumber='691000000',photo=url5)
        freelancer5= Freelancer.objects.create(profile=profile5,profession='Test GraphicprofesionalExperience')
        curriculum3= Curriculum.objects.create(freelancer=freelancer5,verified=True)
        ge=GraphicEngine.objects.create(title="GraphicEngine 10")
        graphicEngineExperience1= GraphicEngineExperience.objects.create(id= 521, curriculum=curriculum3, graphicEngine=ge, graphicExperience=70)
        self.assertEqual(graphicEngineExperience1.id, 521)

    def test_HTML5_Showcase(self):
        user6 = User.objects.create_user(username='userHTML5Test', password='userHTML5Pass')
        url6=URL.objects.create(uri="http://www.pruebasHTML5.com")
        profile6= Profile(user=user6, name='AntonioP', surname='ArenasE', email='antonioc@test.com', city='Sevilla', 
            postalCode='41008', idCardNumber='12345678A', dateOfBirth='1990-12-12 00:00', phoneNumber='691000000',photo=url6)
        freelancer6= Freelancer.objects.create(profile=profile6,profession='Test HTML5')
        curriculum5= Curriculum.objects.create(freelancer=freelancer6,verified=True)
        html5_showcase= HTML5Showcase.objects.create(id= 621, curriculum=curriculum5, embedCode="asdasdasdad")
        self.assertEqual(html5_showcase.id, 621)

    def test_Aptitude(self):
        user7 = User.objects.create_user(username='userAptitudeTest', password='userAptitudePass')
        url7=URL.objects.create(uri="http://www.pruebasAptitude.com")
        profile7= Profile(user=user7, name='AntonioAP', surname='ArenasTI', email='antoniotude@test.com', city='Sevilla', 
            postalCode='41008', idCardNumber='12345678A', dateOfBirth='1990-12-12 00:00', phoneNumber='691000000',photo=url7)
        freelancer7= Freelancer.objects.create(profile=profile7,profession='Test Aptitude')
        curriculum6= Curriculum.objects.create(freelancer=freelancer7,verified=True)
        aptitude1= Aptitude.objects.create(id= 420, curriculum=curriculum6, aptitude="Buen trabajador")
        self.assertEqual(aptitude1.id, 420)

    def test_Link(self):
        user8 = User.objects.create_user(username='userLinkTest', password='userLinkPass')
        url8=URL.objects.create(uri="http://www.pruebasLink.com")
        profile8= Profile(user=user8, name='AntonioL', surname='ArenasI', email='antonionk@test.com', city='Sevilla', 
            postalCode='41008', idCardNumber='12345678A', dateOfBirth='1990-12-12 00:00', phoneNumber='691000000',photo=url8)
        freelancer8= Freelancer.objects.create(profile=profile8,profession='Test Link')
        curriculum6= Curriculum.objects.create(freelancer=freelancer8,verified=True)
        html5_showcase= Link.objects.create(id= 599, curriculum=curriculum6, url="http://www.pruebasLink2.com")
        self.assertEqual(html5_showcase.id, 599)

    def test_Message(self):
        userSender = User.objects.create_user(username='userSenderTest', password='userSenderPass')
        userRecipient = User.objects.create_user(username='userRecipientTest', password='userRecipientPass')
        message= Message.objects.create(id= 1254, sender=userSender,recipient=userRecipient, subject="Asunto",
        text="Texto correo",timestamp=timezone.now,readed=False)
        self.assertEqual(message.id, 1254)