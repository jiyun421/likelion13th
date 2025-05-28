from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class UserManager(BaseUserManager): # 사용자 객체를 생성하고 관리하는 클래스
    def create_user(self, user_id, email, name, generation, gender, password=None): # 일반 사용자 생성
        # 이메일과 이름을 받아 User 객체 생성
        user = self.model(
            user_id=user_id,
            email=self.normalize_email(email),
            name=name,
            generation=generation,
            gender=gender
        )

        user.set_password(password) # 비밀번호 해싱 처리
        user.save(using=self._db) # DB에 저장
        return user

    def create_superuser(self, user_id, email, name, generation, gender, password): # 관리자 생성
        # 일반 유저 생성 후 is_admin = True로 관리자 계정 생성
        user = self.create_user(
            user_id=user_id,
            email=email,
            name=name,
            password=password,
            generation=generation,
            gender=gender
        )

        user.is_admin = True # 관리자 권한 부여
        user.save(using=self._db)
        return user


class User(AbstractBaseUser): # 실제 사용자 정보를 저장하는 모델 클래스
    user_id = models.CharField(max_length=30, unique=True)
    email = models.EmailField(
        verbose_name='email',
        max_length=100,
        unique=True, # 이메일은 고유해야 함
    )
    name = models.CharField(max_length=30)
    generation = models.IntegerField()
    gender = models.CharField(max_length=10)
    is_active = models.BooleanField(default=True) # 계정 활성화 여부
    is_admin = models.BooleanField(default=False) # 관리자 여부 (처음 생성시 false)

    objects = UserManager() # 기본 UserManager 대신 커스텀 UserManager(우리가 커스텀 한 class) 사용

    USERNAME_FIELD = 'user_id' # 로그인 시 user_id를 ID로 사용
    # 기본 User 모델은 username을 사용하지만 우리는 user_id로 변경

    REQUIRED_FIELDS = ['email', 'name', 'generation', 'gender'] # 'createsuperuser' 실행 시 입력해야 할 필드

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None): # 사용자가 특정 권한을 가지고 있는지 확인하는 메서드
        return True # 모든 권한 허용 (추후 수정 가능)

    def has_module_perms(self, app_label):
		    # 사용자가 특정 앱 내에서 하나 이상의 권한을 가지고 있는지 확인하는 메서드
        return True # 모든 앱에 접근 가능 (추후 수정 가능)

    @property
    def is_staff(self): # is_admin이 True이면 is_staff도 True로 설정
        return self.is_admin
    
    class Meta:
        db_table = 'user' # 테이블명을 user로 설정