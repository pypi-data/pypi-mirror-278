from Y3A import Y3A

path = "./src/Demo/Demo.xml"

y3a = Y3A("PE", path)

y3a.fetch("IAM_Role")

y3a.save()

# res = y3a.source("ALL")
# with open('./src/Demo/source.txt', 'w') as file:
#     file.write(res)

res = y3a.html("ALL")
with open('./src/Demo/Demo.html', 'w') as file:
    file.write(res)
