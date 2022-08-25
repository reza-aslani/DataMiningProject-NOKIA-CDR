
import readCDR
import glob
# import networkx as nx

# g = nx.Graph()

# 9131279939
# 9910540287

# خواندن همه فایلهای CDR - در حدود 50000 رکورد وتشکیل فایل csv برای تستهای بعدی
out = open('c:/.dev/cdr-b.csv', 'wt')
for fName in glob.glob("C:/.dev/CHU/chub/*"):
    print(fName)
    readCDR.readFile(fName, out) #, g)
out.close()
 
# #خواندن از فایل csv بدست آمده برای تست های دوم ب بعد برای افزایش سرعت
# readCDR.readCSV('./CDR/CDR.csv',g)

# # # ذخیره کردن با فرمت graphml
# nx.write_graphml(g, "./fullGraph.graphml")

# # فیلتر کردن درجه های بیشتر از دو به اضافه همسایگان آنها
# g2 = nx.Graph()
# for n in [n for n in g if g.degree(n) >= 2]:
#     g2.add_node(n)
#     g2.add_nodes_from(g.neighbors(n))
#     eArr = g.edges(n)
#     g2.add_edges_from(eArr) 

# # ذخیره فیلتر شده ها
# nx.write_graphml(g2, "./degMoreThan1.graphml")

# core2=nx.k_core(g,2)
# nx.write_graphml(core2, "./2-core.graphml")

# core3=nx.k_core(g,3)
# nx.write_graphml(core3, "./3-core.graphml")

# cl=nx.find_cliques(g)
# arr=[n for n in cl]

print('completed !!!!!!!!!!!!!!!!!!!!!!')



# # نمایش گرافیکی گراف حاصله
# import matplotlib.pyplot as plt
# # plt.subplot(121)
# # nx.draw(g, with_labels=True, font_weight='bold')
# # plt.subplot(122)
# pos = nx.spring_layout(g2)
# nx.draw_networkx_nodes(g2, pos, cmap=plt.get_cmap('jet'))
# plt.show()
