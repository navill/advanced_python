class MyClass:
    __secret_value = 1


mc = MyClass()
# print(mc.__secret_value)  # raise error
# print(dir(mc))
print(mc._MyClass__secret_value)  # 1
print(dir(mc))

# 속성에 접근하기 위한 방법
print(mc.__dict__.values())
print(mc.__getattribute__('_MyClass__secret_value'))
# instance의 속성이 descriptor인지 검증 -> if False: __dict__에서 해당 속성을 검색
# -> non-data descriptor(__get__만 구현된 descriptor)인지 확인
# data descriptor > __dict__ > non-data descriptor 순으로 해당 속성을 검색한다.

print(getattr(mc, '_MyClass__secret_value'))
print(mc._MyClass__secret_value)
