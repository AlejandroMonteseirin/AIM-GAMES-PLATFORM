from django.test import TestCase
from AIM_GAMES.models import *
from django.utils import timezone
from .forms import *
# Create your tests here.

class AIM_GAMES_TestCase(TestCase):
    
    def test_tag(self):
        tag=Tag.objects.create(title="Tag 1")
        self.assertEqual(tag.title, 'Tag 1')

    def test_graphicEngine(self):
        ge=GraphicEngine.objects.create(title="GraphicEngine 1")
        self.assertEqual(ge.title, 'GraphicEngine 1')
    
    def test_url(self):
        url=URL.objects.create(id=1000,uri="http://www.pruebas.com")
        self.assertEqual(url.id, 1000)

    def test_Profile(self):
        user1 = User.objects.create_user(username='userProfileTest', password='userProfilePass')
        url1=URL.objects.create(uri="http://www.pruebas.com")
        profile1= Profile.objects.create(id=1001,user=user1, name='Antonio', surname='Arenas', email='antonio@test.com', city='Sevilla', 
            postalCode='41008', idCardNumber='12345678A', dateOfBirth='1990-12-12 00:00', phoneNumber='691000000',photo=url1)
        self.assertEqual(profile1.id, 1001)

    def test_valid_Profile(self):
        user1 = User.objects.create_user(username='userProfileTest2', password='userProfilePass2')
        url1=URL.objects.create(uri="http://www.pruebas.com")
        profile1= Profile.objects.create(user=user1, name='Antonio', surname='Arenas', email='antonio@test.com', city='Sevilla', 
            postalCode='41008', idCardNumber='12345678Z', dateOfBirth='1990-12-12 00:00', phoneNumber='691000000',photo=url1)
        data = {'user': profile1.user, 'name': profile1.name, 'surname': profile1.surname, 'email': profile1.email, 'city': profile1.city, 
        'postalCode': profile1.postalCode, 'idCardNumber': profile1.idCardNumber, 'dateOfBirth': profile1.dateOfBirth, 'phoneNumber': profile1.phoneNumber, 
        'photo': profile1.photo,}
        form = ProfileForm(data=data)
        self.assertTrue(form.is_valid())

    def test_valid_ProfileNoURL(self):
        user1 = User.objects.create_user(username='userProfileTest2', password='userProfilePass2')
        url1=URL.objects.create(uri="http://www.pruebas.com")
        profile1= Profile.objects.create(user=user1, name='Antonio', surname='Arenas', email='antonio@test.com', city='Sevilla', 
            postalCode='41008', idCardNumber='12345678Z', dateOfBirth='1990-12-12 00:00', phoneNumber='691000000')
        data = {'user': profile1.user, 'name': profile1.name, 'surname': profile1.surname, 'email': profile1.email, 'city': profile1.city, 
        'postalCode': profile1.postalCode, 'idCardNumber': profile1.idCardNumber, 'dateOfBirth': profile1.dateOfBirth, 'phoneNumber': profile1.phoneNumber,}
        form = ProfileForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_ProfilePhoneNumberNotDigit(self):
        user1 = User.objects.create_user(username='userProfileTest3', password='userProfilePass3')
        url1=URL.objects.create(uri="http://www.pruebas3.com")
        profile1= Profile.objects.create(user=user1, name='Antonio', surname='Arenas', email='antonio@test.com', city='Sevilla', 
            postalCode='41008', idCardNumber='12345678Z', dateOfBirth='1990-12-12 00:00', phoneNumber='nophone',photo=url1)
        data = {'user': profile1.user, 'name': profile1.name, 'surname': profile1.surname, 'email': profile1.email, 'city': profile1.city, 
        'postalCode': profile1.postalCode, 'idCardNumber': profile1.idCardNumber, 'dateOfBirth': profile1.dateOfBirth, 'phoneNumber': profile1.phoneNumber, 
        'photo': profile1.photo,}
        form = ProfileForm(data=data)
        self.assertFalse(form.is_valid())

    def test_invalid_ProfilePhoneNumberWrongDigit(self):
        user1 = User.objects.create_user(username='userProfileTest3', password='userProfilePass3')
        url1=URL.objects.create(uri="http://www.pruebas3.com")
        profile1= Profile.objects.create(user=user1, name='Antonio', surname='Arenas', email='antonio@test.com', city='Sevilla', 
            postalCode='41008', idCardNumber='12345678Z', dateOfBirth='1990-12-12 00:00', phoneNumber='95486512',photo=url1)
        data = {'user': profile1.user, 'name': profile1.name, 'surname': profile1.surname, 'email': profile1.email, 'city': profile1.city, 
        'postalCode': profile1.postalCode, 'idCardNumber': profile1.idCardNumber, 'dateOfBirth': profile1.dateOfBirth, 'phoneNumber': profile1.phoneNumber, 
        'photo': profile1.photo,}
        form = ProfileForm(data=data)
        self.assertFalse(form.is_valid())

    def test_invalid_ProfilePostalCodeNotDigit(self):
        user1 = User.objects.create_user(username='userProfileTest3', password='userProfilePass3')
        url1=URL.objects.create(uri="http://www.pruebas3.com")
        profile1= Profile.objects.create(user=user1, name='Antonio', surname='Arenas', email='antonio@test.com', city='Sevilla', 
            postalCode='nonCode', idCardNumber='12345678Z', dateOfBirth='1990-12-12 00:00', phoneNumber='987456321',photo=url1)
        data = {'user': profile1.user, 'name': profile1.name, 'surname': profile1.surname, 'email': profile1.email, 'city': profile1.city, 
        'postalCode': profile1.postalCode, 'idCardNumber': profile1.idCardNumber, 'dateOfBirth': profile1.dateOfBirth, 'phoneNumber': profile1.phoneNumber, 
        'photo': profile1.photo,}
        form = ProfileForm(data=data)
        self.assertFalse(form.is_valid())

    def test_invalid_ProfilePostalCodeWrongDigit(self):
        user1 = User.objects.create_user(username='userProfileTest3', password='userProfilePass3')
        url1=URL.objects.create(uri="http://www.pruebas3.com")
        profile1= Profile.objects.create(user=user1, name='Antonio', surname='Arenas', email='antonio@test.com', city='Sevilla', 
            postalCode='4100', idCardNumber='12345678Z', dateOfBirth='1990-12-12 00:00', phoneNumber='987456321',photo=url1)
        data = {'user': profile1.user, 'name': profile1.name, 'surname': profile1.surname, 'email': profile1.email, 'city': profile1.city, 
        'postalCode': profile1.postalCode, 'idCardNumber': profile1.idCardNumber, 'dateOfBirth': profile1.dateOfBirth, 'phoneNumber': profile1.phoneNumber, 
        'photo': profile1.photo,}
        form = ProfileForm(data=data)
        self.assertFalse(form.is_valid())

    def test_invalid_ProfileIDCardNumber(self):
        user1 = User.objects.create_user(username='userProfileTest3', password='userProfilePass3')
        url1=URL.objects.create(uri="http://www.pruebas3.com")
        profile1= Profile.objects.create(user=user1, name='Antonio', surname='Arenas', email='antonio@test.com', city='Sevilla', 
            postalCode='4100', idCardNumber='12345678A', dateOfBirth='1990-12-12 00:00', phoneNumber='987456321',photo=url1)
        data = {'user': profile1.user, 'name': profile1.name, 'surname': profile1.surname, 'email': profile1.email, 'city': profile1.city, 
        'postalCode': profile1.postalCode, 'idCardNumber': profile1.idCardNumber, 'dateOfBirth': profile1.dateOfBirth, 'phoneNumber': profile1.phoneNumber, 
        'photo': profile1.photo,}
        form = ProfileForm(data=data)
        self.assertFalse(form.is_valid())

    def test_invalid_ProfileDateOfBirth(self):
        user1 = User.objects.create_user(username='userProfileTest3', password='userProfilePass3')
        url1=URL.objects.create(uri="http://www.pruebas3.com")
        profile1= Profile.objects.create(user=user1, name='Antonio', surname='Arenas', email='antonio@test.com', city='Sevilla', 
            postalCode='4100', idCardNumber='12345678A', dateOfBirth='2012-12-12 00:00', phoneNumber='987456321',photo=url1)
        data = {'user': profile1.user, 'name': profile1.name, 'surname': profile1.surname, 'email': profile1.email, 'city': profile1.city, 
        'postalCode': profile1.postalCode, 'idCardNumber': profile1.idCardNumber, 'dateOfBirth': profile1.dateOfBirth, 'phoneNumber': profile1.phoneNumber, 
        'photo': profile1.photo,}
        form = ProfileForm(data=data)
        self.assertFalse(form.is_valid())
    
    def test_Freelancer(self):
        user2 = User.objects.create_user(username='userFreelancerTest', password='userFreelancerPass')
        url2=URL.objects.create(uri="http://www.pruebas.com")
        profile2= Profile.objects.create(id=1002,user=user2, name='AntonioF', surname='ArenasF', email='antoniof@test.com', city='Sevilla', 
            postalCode='41008', idCardNumber='12345678A', dateOfBirth='1990-12-12 00:00', phoneNumber='691000000',photo=url2)
        freelancer1= Freelancer.objects.create(id=1003,profile=profile2,profession='Test profesion')
        self.assertEqual(freelancer1.id, 1003)

    def test_valid_Freelancer(self):
        user1 = User.objects.create_user(username='userProfileTest2', password='userProfilePass2')
        url1=URL.objects.create(uri="http://www.pruebas.com")
        profile1= Profile.objects.create(user=user1, name='Antonio', surname='Arenas', email='antonio@test.com', city='Sevilla', 
            postalCode='41008', idCardNumber='12345678Z', dateOfBirth='1990-12-12 00:00', phoneNumber='691000000',photo=url1)
        freelancer1= Freelancer.objects.create(profile=profile1,profession='Test profesion')
        data = {'profile': freelancer1.profile, 'profession': freelancer1.profession,}
        form = FreelancerForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_Freelancer(self):
        # Profile inválido
        user1 = User.objects.create_user(username='userProfileTest3', password='userProfilePass3')
        url1=URL.objects.create(uri="http://www.pruebas3.com")
        profile1= Profile.objects.create(user=user1, name='Antonio', surname='Arenas', email='antonio@test.com', city='Sevilla', 
            postalCode='4100', idCardNumber='12345678A', dateOfBirth='2012-12-12 00:00', phoneNumber='987456321',photo=url1)
        freelancer1= Freelancer.objects.create(profile=profile1,profession='Test profesion')
        data = {'profile': freelancer1.profile, 'profession': freelancer1.profession,}
        form = FreelancerForm(data=data)
        self.assertFalse(form.is_valid())

    def test_Manager(self):
        user3 = User.objects.create_user(username='userBusinessTest', password='userBusinessPass')
        url3=URL.objects.create(uri="http://www.pruebas.com")
        profile3= Profile.objects.create(user=user3, name='AntonioF', surname='ArenasF', email='antoniof@test.com', city='Sevilla', 
            postalCode='41008', idCardNumber='12345678A', dateOfBirth='1990-12-12 00:00', phoneNumber='691000000',photo=url3)
        manager1= Manager.objects.create(id=1004,profile=profile3)
        self.assertEqual(manager1.id, 1004)

    def test_Curriculum(self):
        user4 = User.objects.create_user(username='userCurriculumTest', password='userCurriculumPass')
        url4=URL.objects.create(uri="http://www.pruebasC.com")
        profile4= Profile.objects.create(user=user4, name='AntonioC', surname='ArenasC', email='antonioc@test.com', city='Sevilla', 
            postalCode='41008', idCardNumber='12345678A', dateOfBirth='1990-12-12 00:00', phoneNumber='691000000',photo=url4)
        freelancer4= Freelancer.objects.create(profile=profile4,profession='Test curriculum')
        curriculum1= Curriculum.objects.create(id= 1005,freelancer=freelancer4,verified=True)
        self.assertEqual(curriculum1.id, 1005)

    def test_Profesional_Experience(self):
        user5 = User.objects.create_user(username='userPExperienceTest', password='userPExperiencePass')
        url5=URL.objects.create(uri="http://www.pruebasPE.com")
        profile5= Profile.objects.create(user=user5, name='AntonioP', surname='ArenasE', email='antoniope@test.com', city='Sevilla', 
            postalCode='41008', idCardNumber='12345678A', dateOfBirth='1990-12-12 00:00', phoneNumber='691000000',photo=url5)
        freelancer5= Freelancer.objects.create(profile=profile5,profession='Test profesionalExperience')
        curriculum1= Curriculum.objects.create(freelancer=freelancer5,verified=True)
        professionalExperience1= ProfessionalExperience.objects.create(id= 1006, curriculum=curriculum1, center='CentroPRueba', formation="FormacionPrueba",
        startDate="2017-01-13", endDate="2019-01-10", miniature="http://www.miniature.com")
        self.assertEqual(professionalExperience1.id, 1006)

    def test_valid_Profesional_Experience(self):
        user1 = User.objects.create_user(username='userProfileTest2', password='userProfilePass2')
        url1=URL.objects.create(uri="http://www.pruebas.com")
        profile1= Profile.objects.create(user=user1, name='Antonio', surname='Arenas', email='antonio@test.com', city='Sevilla', 
            postalCode='41008', idCardNumber='12345678Z', dateOfBirth='1990-12-12 00:00', phoneNumber='691000000',photo=url1)
        freelancer1= Freelancer.objects.create(profile=profile1,profession='Test profesion')
        curriculum1= Curriculum.objects.create(freelancer=freelancer1,verified=True)
        professionalExperience1= ProfessionalExperience.objects.create(curriculum=curriculum1, center='CentroPRueba', formation="FormacionPrueba",
        startDate="2017-01-13", endDate="2019-01-10", miniature="http://www.miniature.com")
        data = {'curriculum': professionalExperience1.curriculum, 'center': professionalExperience1.center, 'formation': professionalExperience1.formation,
        'startDate': professionalExperience1.startDate, 'endDate': professionalExperience1.endDate, 'miniature': professionalExperience1.miniature,}
        form = ProfessionalExperienceForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_Profesional_Experience(self):
        # Fecha fin inexistente
        user1 = User.objects.create_user(username='userProfileTest2', password='userProfilePass2')
        url1=URL.objects.create(uri="http://www.pruebas.com")
        profile1= Profile.objects.create(user=user1, name='Antonio', surname='Arenas', email='antonio@test.com', city='Sevilla', 
            postalCode='41008', idCardNumber='12345678Z', dateOfBirth='1990-12-12 00:00', phoneNumber='691000000',photo=url1)
        freelancer1= Freelancer.objects.create(profile=profile1,profession='Test profesion')
        curriculum1= Curriculum.objects.create(freelancer=freelancer1,verified=True)
        professionalExperience1= ProfessionalExperience.objects.create(curriculum=curriculum1, center='CentroPRueba', formation="FormacionPrueba",
        startDate="2017-01-13", endDate="2019-01-10", miniature="http://www.miniature.com")
        data = {'curriculum': professionalExperience1.curriculum, 'center': professionalExperience1.center, 'formation': professionalExperience1.formation,
        'startDate': professionalExperience1.startDate, 'miniature': professionalExperience1.miniature,}
        form = ProfessionalExperienceForm(data=data)
        self.assertFalse(form.is_valid())

    def test_GraphicEngine_Experience(self):
        user5 = User.objects.create_user(username='userGEExperienceTest', password='userGEExperiencePass')
        url5=URL.objects.create(uri="http://www.pruebasGEE.com")
        profile5= Profile.objects.create(user=user5, name='AntonioG', surname='ArenasEE', email='antonioGEE@test.com', city='Sevilla', 
            postalCode='41008', idCardNumber='12345678A', dateOfBirth='1990-12-12 00:00', phoneNumber='691000000',photo=url5)
        freelancer5= Freelancer.objects.create(profile=profile5,profession='Test GraphicprofesionalExperience')
        curriculum3= Curriculum.objects.create(freelancer=freelancer5,verified=True)
        ge=GraphicEngine.objects.create(title="GraphicEngine 10")
        graphicEngineExperience1= GraphicEngineExperience.objects.create(id= 1007, curriculum=curriculum3, graphicEngine=ge, graphicExperience=70)
        self.assertEqual(graphicEngineExperience1.id, 1007)

    def test_valid_GraphicEngine_Experience(self):
        user1 = User.objects.create_user(username='userProfileTest2', password='userProfilePass2')
        url1=URL.objects.create(uri="http://www.pruebas.com")
        profile1= Profile.objects.create(user=user1, name='Antonio', surname='Arenas', email='antonio@test.com', city='Sevilla', 
            postalCode='41008', idCardNumber='12345678Z', dateOfBirth='1990-12-12 00:00', phoneNumber='691000000',photo=url1)
        freelancer1= Freelancer.objects.create(profile=profile1,profession='Test profesion')
        curriculum1= Curriculum.objects.create(freelancer=freelancer1,verified=True)
        ge=GraphicEngine.objects.create(title="GraphicEngine 10")
        graphicEngineExperience1= GraphicEngineExperience.objects.create(curriculum=curriculum1, graphicEngine=ge, graphicExperience=70)
        data = {'curriculum': graphicEngineExperience1.curriculum, 'graphicEngine': graphicEngineExperience1.graphicEngine, 
        'graphicExperience': graphicEngineExperience1.graphicExperience,}
        form = GraphicEngineExperienceForm(data=data)
        self.assertTrue(form.is_valid())

    def test_valid_GraphicEngine_Experience(self):
        #Probando el rango justo en los limites
        user1 = User.objects.create_user(username='userProfileTest2', password='userProfilePass2')
        url1=URL.objects.create(uri="http://www.pruebas.com")
        profile1= Profile.objects.create(user=user1, name='Antonio', surname='Arenas', email='antonio@test.com', city='Sevilla', 
            postalCode='41008', idCardNumber='12345678Z', dateOfBirth='1990-12-12 00:00', phoneNumber='691000000',photo=url1)
        freelancer1= Freelancer.objects.create(profile=profile1,profession='Test profesion')
        curriculum1= Curriculum.objects.create(freelancer=freelancer1,verified=True)
        ge=GraphicEngine.objects.create(title="GraphicEngine 10")
        graphicEngineExperience1= GraphicEngineExperience.objects.create(curriculum=curriculum1, graphicEngine=ge, graphicExperience=0)
        data = {'curriculum': graphicEngineExperience1.curriculum, 'graphicEngine': graphicEngineExperience1.graphicEngine, 
        'graphicExperience': graphicEngineExperience1.graphicExperience,}
        form = GraphicEngineExperienceForm(data=data)
        self.assertTrue(form.is_valid())

    def test_valid_GraphicEngine_Experience(self):
        #Probando el rango justo en los limites
        user1 = User.objects.create_user(username='userProfileTest2', password='userProfilePass2')
        url1=URL.objects.create(uri="http://www.pruebas.com")
        profile1= Profile.objects.create(user=user1, name='Antonio', surname='Arenas', email='antonio@test.com', city='Sevilla', 
            postalCode='41008', idCardNumber='12345678Z', dateOfBirth='1990-12-12 00:00', phoneNumber='691000000',photo=url1)
        freelancer1= Freelancer.objects.create(profile=profile1,profession='Test profesion')
        curriculum1= Curriculum.objects.create(freelancer=freelancer1,verified=True)
        ge=GraphicEngine.objects.create(title="GraphicEngine 10")
        graphicEngineExperience1= GraphicEngineExperience.objects.create(curriculum=curriculum1, graphicEngine=ge, graphicExperience=1)
        data = {'curriculum': graphicEngineExperience1.curriculum, 'graphicEngine': graphicEngineExperience1.graphicEngine, 
        'graphicExperience': graphicEngineExperience1.graphicExperience,}
        form = GraphicEngineExperienceForm(data=data)
        self.assertTrue(form.is_valid())

    def test_valid_GraphicEngine_Experience(self):
        #Probando el rango justo en los limites
        user1 = User.objects.create_user(username='userProfileTest2', password='userProfilePass2')
        url1=URL.objects.create(uri="http://www.pruebas.com")
        profile1= Profile.objects.create(user=user1, name='Antonio', surname='Arenas', email='antonio@test.com', city='Sevilla', 
            postalCode='41008', idCardNumber='12345678Z', dateOfBirth='1990-12-12 00:00', phoneNumber='691000000',photo=url1)
        freelancer1= Freelancer.objects.create(profile=profile1,profession='Test profesion')
        curriculum1= Curriculum.objects.create(freelancer=freelancer1,verified=True)
        ge=GraphicEngine.objects.create(title="GraphicEngine 10")
        graphicEngineExperience1= GraphicEngineExperience.objects.create(curriculum=curriculum1, graphicEngine=ge, graphicExperience=99)
        data = {'curriculum': graphicEngineExperience1.curriculum, 'graphicEngine': graphicEngineExperience1.graphicEngine, 
        'graphicExperience': graphicEngineExperience1.graphicExperience,}
        form = GraphicEngineExperienceForm(data=data)
        self.assertTrue(form.is_valid())

    def test_valid_GraphicEngine_Experience(self):
        #Probando el rango justo en los limites
        user1 = User.objects.create_user(username='userProfileTest2', password='userProfilePass2')
        url1=URL.objects.create(uri="http://www.pruebas.com")
        profile1= Profile.objects.create(user=user1, name='Antonio', surname='Arenas', email='antonio@test.com', city='Sevilla', 
            postalCode='41008', idCardNumber='12345678Z', dateOfBirth='1990-12-12 00:00', phoneNumber='691000000',photo=url1)
        freelancer1= Freelancer.objects.create(profile=profile1,profession='Test profesion')
        curriculum1= Curriculum.objects.create(freelancer=freelancer1,verified=True)
        ge=GraphicEngine.objects.create(title="GraphicEngine 10")
        graphicEngineExperience1= GraphicEngineExperience.objects.create(curriculum=curriculum1, graphicEngine=ge, graphicExperience=100)
        data = {'curriculum': graphicEngineExperience1.curriculum, 'graphicEngine': graphicEngineExperience1.graphicEngine, 
        'graphicExperience': graphicEngineExperience1.graphicExperience,}
        form = GraphicEngineExperienceForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_GraphicEngine_Experience(self):
        # Valor -1 (rango 0 a 100)
        user1 = User.objects.create_user(username='userProfileTest2', password='userProfilePass2')
        url1=URL.objects.create(uri="http://www.pruebas.com")
        profile1= Profile.objects.create(user=user1, name='Antonio', surname='Arenas', email='antonio@test.com', city='Sevilla', 
            postalCode='41008', idCardNumber='12345678Z', dateOfBirth='1990-12-12 00:00', phoneNumber='691000000',photo=url1)
        freelancer1= Freelancer.objects.create(profile=profile1,profession='Test profesion')
        curriculum1= Curriculum.objects.create(freelancer=freelancer1,verified=True)
        ge=GraphicEngine.objects.create(title="GraphicEngine 10")
        graphicEngineExperience1= GraphicEngineExperience.objects.create(curriculum=curriculum1, graphicEngine=ge, graphicExperience=-1)
        data = {'curriculum': graphicEngineExperience1.curriculum, 'graphicEngine': graphicEngineExperience1.graphicEngine, 
        'graphicExperience': graphicEngineExperience1.graphicExperience,}
        form = GraphicEngineExperienceForm(data=data)
        self.assertFalse(form.is_valid())

    def test_invalid_GraphicEngine_Experience(self):
        # Valor 101 (rango 0 a 100)
        user1 = User.objects.create_user(username='userProfileTest2', password='userProfilePass2')
        url1=URL.objects.create(uri="http://www.pruebas.com")
        profile1= Profile.objects.create(user=user1, name='Antonio', surname='Arenas', email='antonio@test.com', city='Sevilla', 
            postalCode='41008', idCardNumber='12345678Z', dateOfBirth='1990-12-12 00:00', phoneNumber='691000000',photo=url1)
        freelancer1= Freelancer.objects.create(profile=profile1,profession='Test profesion')
        curriculum1= Curriculum.objects.create(freelancer=freelancer1,verified=True)
        ge=GraphicEngine.objects.create(title="GraphicEngine 10")
        graphicEngineExperience1= GraphicEngineExperience.objects.create(curriculum=curriculum1, graphicEngine=ge, graphicExperience=101)
        data = {'curriculum': graphicEngineExperience1.curriculum, 'graphicEngine': graphicEngineExperience1.graphicEngine, 
        'graphicExperience': graphicEngineExperience1.graphicExperience,}
        form = GraphicEngineExperienceForm(data=data)
        self.assertFalse(form.is_valid())



    def test_HTML5_Showcase(self):
        user6 = User.objects.create_user(username='userHTML5Test', password='userHTML5Pass')
        url6=URL.objects.create(uri="http://www.pruebasHTML5.com")
        profile6= Profile.objects.create(user=user6, name='AntonioP', surname='ArenasE', email='antonioc@test.com', city='Sevilla', 
            postalCode='41008', idCardNumber='12345678A', dateOfBirth='1990-12-12 00:00', phoneNumber='691000000',photo=url6)
        freelancer6= Freelancer.objects.create(profile=profile6,profession='Test HTML5')
        curriculum5= Curriculum.objects.create(freelancer=freelancer6,verified=True)
        html5_showcase= HTML5Showcase.objects.create(id= 1008, curriculum=curriculum5, embedCode="asdasdasdad")
        self.assertEqual(html5_showcase.id, 1008)

    def test_Aptitude(self):
        user7 = User.objects.create_user(username='userAptitudeTest', password='userAptitudePass')
        url7=URL.objects.create(uri="http://www.pruebasAptitude.com")
        profile7= Profile.objects.create(user=user7, name='AntonioAP', surname='ArenasTI', email='antoniotude@test.com', city='Sevilla', 
            postalCode='41008', idCardNumber='12345678A', dateOfBirth='1990-12-12 00:00', phoneNumber='691000000',photo=url7)
        freelancer7= Freelancer.objects.create(profile=profile7,profession='Test Aptitude')
        curriculum6= Curriculum.objects.create(freelancer=freelancer7,verified=True)
        aptitude1= Aptitude.objects.create(id= 1009, curriculum=curriculum6, aptitude="Buen trabajador")
        self.assertEqual(aptitude1.id, 1009)

    def test_valid_Aptitude(self):
        user1 = User.objects.create_user(username='userProfileTest2', password='userProfilePass2')
        url1=URL.objects.create(uri="http://www.pruebas.com")
        profile1= Profile.objects.create(user=user1, name='Antonio', surname='Arenas', email='antonio@test.com', city='Sevilla', 
            postalCode='41008', idCardNumber='12345678Z', dateOfBirth='1990-12-12 00:00', phoneNumber='691000000',photo=url1)
        freelancer1= Freelancer.objects.create(profile=profile1,profession='Test profesion')
        curriculum1= Curriculum.objects.create(freelancer=freelancer1,verified=True)
        aptitude1= Aptitude.objects.create(curriculum=curriculum1, aptitude="Buen trabajador")
        data = {'curriculum': aptitude1.curriculum, 'aptitude': aptitude1.aptitude,}
        form = AptitudeForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_Aptitude(self):
        # Atributo aptitude inexistente
        user1 = User.objects.create_user(username='userProfileTest2', password='userProfilePass2')
        url1=URL.objects.create(uri="http://www.pruebas.com")
        profile1= Profile.objects.create(user=user1, name='Antonio', surname='Arenas', email='antonio@test.com', city='Sevilla', 
            postalCode='41008', idCardNumber='12345678Z', dateOfBirth='1990-12-12 00:00', phoneNumber='691000000',photo=url1)
        freelancer1= Freelancer.objects.create(profile=profile1,profession='Test profesion')
        curriculum1= Curriculum.objects.create(freelancer=freelancer1,verified=True)
        aptitude1= Aptitude.objects.create(curriculum=curriculum1, aptitude="Buen trabajador")
        data = {'curriculum': aptitude1.curriculum,}
        form = AptitudeForm(data=data)
        self.assertFalse(form.is_valid())
    

    def test_Link(self):
        user8 = User.objects.create_user(username='userLinkTest', password='userLinkPass')
        url8=URL.objects.create(uri="http://www.pruebasLink.com")
        profile8= Profile.objects.create(user=user8, name='AntonioL', surname='ArenasI', email='antonionk@test.com', city='Sevilla', 
            postalCode='41008', idCardNumber='12345678A', dateOfBirth='1990-12-12 00:00', phoneNumber='691000000',photo=url8)
        freelancer8= Freelancer.objects.create(profile=profile8,profession='Test Link')
        curriculum6= Curriculum.objects.create(freelancer=freelancer8,verified=True)
        link= Link.objects.create(id= 1010, curriculum=curriculum6, url="http://www.pruebasLink2.com")
        self.assertEqual(link.id, 1010)

    def test_valid_Link(self):
        user1 = User.objects.create_user(username='userProfileTest2', password='userProfilePass2')
        url1=URL.objects.create(uri="http://www.pruebas.com")
        profile1= Profile.objects.create(user=user1, name='Antonio', surname='Arenas', email='antonio@test.com', city='Sevilla', 
            postalCode='41008', idCardNumber='12345678Z', dateOfBirth='1990-12-12 00:00', phoneNumber='691000000',photo=url1)
        freelancer1= Freelancer.objects.create(profile=profile1,profession='Test profesion')
        curriculum1= Curriculum.objects.create(freelancer=freelancer1,verified=True)
        link= Link.objects.create(curriculum=curriculum1, url="http://www.pruebasLink2.com")
        data = {'curriculum': link.curriculum, 'url': link.url,}
        form = LinkForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_Link(self):
        # Atributo URL inexistente
        user1 = User.objects.create_user(username='userProfileTest2', password='userProfilePass2')
        url1=URL.objects.create(uri="http://www.pruebas.com")
        profile1= Profile.objects.create(user=user1, name='Antonio', surname='Arenas', email='antonio@test.com', city='Sevilla', 
            postalCode='41008', idCardNumber='12345678Z', dateOfBirth='1990-12-12 00:00', phoneNumber='691000000',photo=url1)
        freelancer1= Freelancer.objects.create(profile=profile1,profession='Test profesion')
        curriculum1= Curriculum.objects.create(freelancer=freelancer1,verified=True)
        link= Link.objects.create(curriculum=curriculum1, url="http://www.pruebasLink2.com")
        data = {'curriculum': link.curriculum,}
        form = LinkForm(data=data)
        self.assertFalse(form.is_valid())

    def test_Message(self):
        userSender = User.objects.create_user(username='userSenderTest', password='userSenderPass')
        userRecipient = User.objects.create_user(username='userRecipientTest', password='userRecipientPass')
        message= Message.objects.create(id= 1011, sender=userSender,recipient=userRecipient, subject="Asunto",
        text="Texto correo",timestamp='2018-12-12 00:00',readed=False)
        self.assertEqual(message.id, 1011)

    def test_valid_Message(self):
        userSender = User.objects.create_user(username='userSenderTest', password='userSenderPass')
        userRecipient = User.objects.create_user(username='userRecipientTest', password='userRecipientPass')
        message= Message.objects.create(sender=userSender,recipient=userRecipient, subject="Asunto",
        text="Texto correo",timestamp='2018-12-12 00:00',readed=False)
        data = {'sender': message.sender, 'recipient': message.recipient, 'subject': message.subject, 
        'text': message.text, 'timestamp': message.timestamp,'readed': message.readed,}
        form = MessageForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_Message(self):
        # Atributo text inexistente
        userSender = User.objects.create_user(username='userSenderTest', password='userSenderPass')
        userRecipient = User.objects.create_user(username='userRecipientTest', password='userRecipientPass')
        message= Message.objects.create(sender=userSender,recipient=userRecipient, subject="Asunto",
        text="Texto correo",timestamp='2018-12-12 00:00',readed=False)
        data = {'sender': message.sender, 'recipient': message.recipient, 'subject': message.subject, 
        'timestamp': message.timestamp,'readed': message.readed,}
        form = MessageForm(data=data)
        self.assertFalse(form.is_valid())