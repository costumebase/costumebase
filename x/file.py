
bar = ['rafi', 'sifat']

bar.append('rafir')

print(bar)


try:
    name = open('file.csv')
except FileNotFoundError:
    print("File didn't found ")
except Exception as e:
    print(e)

else:
    print("printing succes full code")

    for i in name:
        print(i, "nodeee")

    name.close()

    print("success! ")



# while True:

#     bar = input(str("input your name :"))

#     if bar == 'rafi':
#         break

#     print(bar)
# print("Break the while")
