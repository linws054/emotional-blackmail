import os
from pyltp import Postagger, Segmentor
import pandas as pd
import OpenHowNet
from itertools import product


class LtpParser:
	def __init__(self):
		LTP_DIR = "D:\ltp_data_v3.4.0"
		self.segmentor = Segmentor(os.path.join(LTP_DIR, "cws.model"))
		self.postagger = Postagger(os.path.join(LTP_DIR, "pos.model"))
		OpenHowNet.download()
		self.hownet_dict_advanced = OpenHowNet.HowNetDict(init_sim=True)



	def part1(self, test, train):
		result = 0

		for i in range(2):
			if test[i] == train[i]:
				result = result +1

		#add_result1 = self.part1_sm(train[1], test[1])
		#add_result3 = self.part1_sm(train[3], test[3])
		#result = result + add_result1 + add_result3

		return result



	def part5(self, test6, train6):
		result = [0, list(), list()]
		t6 = train6.split('$')
		t6 = t6[0]
		t6 = t6.split('_')

		te6 = test6.split('$')

		for te in te6:
			if t6[0] in te:
				result[0] = 1
				result[1].append(t6[1])

				tee = te.split('_')
				result[2].append(tee[1])

		return result




	def for_part52(self, test4, ls2_1, ls2_2, ls2_4, ls2_5, ls5_2):

		test_l1 = []
		for l1 in ls2_1:
			zi_tl1 = []
			for i in range(len(test4) - len(l1) + 1):
				pos_zuhe = []
				weizhi_zuhe = []
				for j in range(len(l1)):
					pos_zuhe.append(test4[i + j])
				if pos_zuhe == l1:
					weizhi_zuhe.append(i)
					weizhi_zuhe.append(i + len(l1) - 1)
					zi_tl1.append(weizhi_zuhe)
			test_l1.append(zi_tl1)
		#print("test_l1: ", test_l1)

		#x = 0
		if len(test_l1) > 1:
			ls_hunhe = []
			for i in range(len(test_l1) - 1):
				if i == 0:
					ls_hunhe = test_l1[i]
				ls_hunhe = list(product(ls_hunhe, test_l1[i + 1]))

			new_ls_hunhe = []
			for lh in ls_hunhe:
				self.move_list(lh, new_ls_hunhe)

			jiange = len(ls2_2)
			ls_jiweiyizu = []
			ls = []
			for i in range(len(new_ls_hunhe)):
				if i % jiange == 0:
					if len(ls) > 0:
						ls_jiweiyizu.append(ls)
					ls = []
				ls.append(new_ls_hunhe[i])
				if i == len(new_ls_hunhe) - 1:
					ls_jiweiyizu.append(ls)
			#print("ls_jiweiyizu: ", ls_jiweiyizu)

			ls_fuheyaoqiu = []
			for l_j in ls_jiweiyizu:
				panduan = 1
				for i in range(len(l_j) - 1):
					lji = l_j[i]
					lji1 = l_j[i + 1]
					if lji[1] >= lji1[0]:
						panduan = 0
						break
				if panduan == 1:
					ls_fuheyaoqiu.append(l_j)
			#print("ls_fuheyaoqiu: ", ls_fuheyaoqiu)
		else:
			ls_fuheyaoqiu = test_l1

		ls_zong = []
		for lsf in ls_fuheyaoqiu:
			ls = []
			for i in range(len(ls2_2)):
				ls.append(0)
			ls_range = []
			for i in range(len(ls2_2)):
				ls_range.append(i)

			for i in range(len(ls2_2)):
				result2i = lsf[i]
				for j in range(len(result2i)):
					panduan = 0
					for l52 in ls5_2:
						for r3 in ls2_4:
							if r3 == result2i[j]:
								if int(l52) == result2i[j]:
									ls[i] = 1
									ls_range.remove(i)
									panduan = 1
									break
								else:
									ls[i] = 3
									ls_range.remove(i)
									panduan = 1
									break
						if panduan == 1:
							break
					if panduan == 1:
						break

			for lr in ls_range:
				result2lr = lsf[lr]
				ls_qian = []
				ls_hou = []

				for i in range(result2lr[0] - 1,  -1, -1):
					panduan = 0
					for r3 in ls2_4:
						if r3 == i:
							for l52 in ls5_2:
								if int(l52) == i:
									ls_qian.append([i, 2])
									panduan = 1
									break
								else:
									ls_qian.append([i, 0])
									panduan = 1
									break
					if panduan == 1:
						break

				for i in range(result2lr[-1] + 1, len(test4)):
					panduan = 0
					for r3 in ls2_4:
						if r3 == i:
							for l52 in ls5_2:
								if int(l52) == i:
									ls_hou.append([i, 2])
									panduan = 1
									break
								else:
									ls_hou.append([i, 0])
									panduan = 1
									break
					if panduan == 1:
						break

				if len(ls_qian) > 0 and len(ls_hou) > 0:
					if result2lr[0] - ls_qian[0][0] > ls_hou[0][0] - result2lr[-1]:
						ls[lr] = ls_hou[0][1]
					else:
						ls[lr] = ls_qian[0][1]

				if len(ls_qian) > 0 and len(ls_hou) == 0:
					ls[lr] = ls_qian[0][1]

				if len(ls_qian) == 0 and len(ls_hou) > 0:
					ls[lr] = ls_hou[0][1]

			ls_zong.append(ls)

		final = 0
		for lz in ls_zong:
			count = 0
			for i in range(len(ls2_5)):
				if ls2_5[i] == lz[i]:
					count = count+1
			if final < count:
				final = count

		final = final / len(ls2_5)
		'''
			for i in range(len(ls5_1)):
				ls52 = ls5_2[i]
				#print("ls52: ", ls52)
				for l_j in ls_fuheyaoqiu:
					#不同的全套组合
					num = 0
					for k in range(len(ls2_2)):
						ljk = l_j[k]
						#print("ljk: ", ljk)
						if int(ljk[0]) >= int(ls52) and int(ljk[1]) >= int(ls52) :
							guodu = int(ls52) - int(ljk[0]) - (int(ls5_1[i]) - int(ls2_2[k][0]))
							guodu = guodu * guodu
							guodu = guodu ** 0.5
							#print("guodu:", guodu)
							num = num + guodu / ( ( int(ljk[1])-int(ljk[0])+1 )/2 )	#系数，可调
						if int(ljk[0]) <= int(ls52) and int(ljk[1]) <= int(ls52):
							guodu = int(ls52) - int(ljk[0]) - (int(ls5_1[i]) - int(ls2_2[k][0]))
							guodu = guodu * guodu
							guodu = guodu ** 0.5
							#print("guodu:", guodu)
							num = num + guodu / ((int(ljk[1]) - int(ljk[0]) + 1) / 2)  # 系数，可调
							#if num == 0:
								#print("int(ls52): ", int(ls52))
								#print("ls_fuheyaoqiu: ", ls_fuheyaoqiu)
								#print("int(ls5_1[i]): ", int(ls5_1[i]))
								#print("ls3_2: ", ls2_2)
					if x == 0 or x > num:
						x = num
					#print("x:", x)
		'''
		'''
		if len(ls2_2) > 0:
			x = x / len(ls2_2)
			final = 1 - x * x / len(train4)  # 系数，可调
		if final < 0:
			final = 0
		print("final:", final)
		return final
		'''
		return final



	def part1_sm(self, train1, test1):

		result = 0
		train1 = train1[:-1]
		test1 = test1[:-1]
		tr1 = train1.split("_")
		te1 = test1.split("_")
		if len(tr1) == len(te1):
			result = result + 1
			for i in range(len(tr1)):
				#print(tr1[i], te1[i])
				word_sim = self.hownet_dict_advanced.calculate_word_similarity(tr1[i], te1[i])
				#print(word_sim)
				if word_sim <= 0.73:
					result = result - 1
					break

		return result



	def part2(self, train4, test4, ls51):
		result = [0, list(), list(), list(), list(), list()]

		final = 0

		for i in range(len(test4)-1):
			#print("i: ", i)
			digui = self.digui_part2(0, train4, i, test4, list(), list())
			#print("digui: ", digui)
			jieguo = 0
			if digui[0] == 1:
				for dg in digui[1]:
					jieguo = jieguo + len(dg)
			if final < jieguo:
				final = jieguo
				result[0] = final
				result[1] = digui[1]
				result[2] = digui[2]

		'''
		for i in range(len(train4)-1):
			#print("i: ", i)
			digui = self.digui_part2(i, train4, 0, test4, list(), list())
			#print("digui: ", digui)
			jieguo = 0
			if digui[0] == 1:
				for dg in digui[1]:
					jieguo = jieguo + len(dg)
			if final < jieguo:
				final = jieguo
				result[0] = final
				result[1] = digui[1]
				result[2] = digui[2]
		'''
		final = final / len(train4)
		result[0] = final

		print("result[1]: ", result[1])
		print("train4: ", train4)

		for i in range(len(train4)):
			if train4[i] == 'r':
				result[3].append(i)
		for i in range(len(test4)):
			if test4[i] == 'r':
				result[4].append(i)

		ls = []
		for i in range(len(result[2])):
			ls.append(0)

		ls_range = []
		for i in range(len(result[2])):
			ls_range.append(i)

		for i in range(len(result[2])):
			result2i = result[2][i]
			for j in range(len(result2i)):
				panduan = 0
				for r3 in result[3]:
					if r3 == result2i[j]:
						if int(ls51[0]) == result2i[j]:
							ls[i] = 1
							ls_range.remove(i)
							panduan = 1
							break
						else:
							ls[i] = 3
							ls_range.remove(i)
							panduan = 1
							break
				if panduan == 1:
					break

		for lr in ls_range:
			result2lr = result[2][lr]
			ls_qian = []
			ls_hou = []

			for i in range(result2lr[0]-1, -1, -1):
				panduan = 0
				for r3 in result[3]:
					if r3 == i:
						if int(ls51[0]) == i:
							ls_qian.append([i, 2])
							panduan = 1
							break
						else:
							ls_qian.append([i, 0])
							panduan = 1
							break
				if panduan == 1:
					break

			for i in range(result2lr[-1]+1, len(train4)):
				panduan = 0
				for r3 in result[3]:
					if r3 == i:
						if int(ls51[0]) == i:
							ls_hou.append([i, 2])
							panduan = 1
							break
						else:
							ls_hou.append([i, 0])
							panduan = 1
							break
				if panduan == 1:
					break

			if len(ls_qian) > 0 and len(ls_hou) > 0:
				if result2lr[0]-ls_qian[0][0] > ls_hou[0][0]-result2lr[-1]:
					ls[lr] = ls_hou[0][1]
				else:
					ls[lr] = ls_qian[0][1]

			if len(ls_qian) > 0 and len(ls_hou) == 0:
				ls[lr] = ls_qian[0][1]

			if len(ls_qian) == 0 and len(ls_hou) > 0:
				ls[lr] = ls_hou[0][1]

		result[5] = ls

		return result



	def digui_part2(self, weizhi1, train4, weizhi2, test4, ls1, ls2):
		#test4, train4已经-1并split过
		#print("weizhi2: ", weizhi2)
		#print("len(test4)-1: ", len(test4)-1)
		#print("weizhi1: ", weizhi1)
		#print("len(train4)-1: ", len(train4) - 1)
		weizhi_1 = 0
		weizhi_21 = 0
		weizhi_22 = 0
		zi_ls1 = []
		zi_ls2 = []
		biaozhi = 0
		for j in range(weizhi1, len(train4) - 1):
			if [test4[weizhi2], test4[weizhi2+1]] == [train4[j], train4[j+1]]:
				weizhi_1 = j + 2
				zi_ls1.append(train4[j])
				zi_ls1.append(train4[j + 1])
				zi_ls2.append(j)
				zi_ls2.append(j + 1)
				break

		if weizhi_1 != 0:
			biaozhi = 1
			if weizhi_1 < len(train4):
				for k in range(weizhi_1, len(train4)):
					if weizhi2 + 2 + k - weizhi_1 < len(test4):
						if train4[k] == test4[weizhi2 + 2 + k - weizhi_1]:
							zi_ls1.append(train4[k])
							zi_ls2.append(k)
						else:
							weizhi_21 = k
							weizhi_22 = weizhi2 + 2 + k - weizhi_1
							break
					else:
						break
			ls1.append(zi_ls1)
			ls2.append(zi_ls2)

		if weizhi_21 != 0:
			if weizhi_21 + 1 < len(train4) - 1:
				if weizhi_22 < len(test4) - 1:

					zi_result = [list(), list()]
					final = 0
					for i in range(weizhi_22, len(test4) - 1):
						# print("weizhi_22: ", weizhi_22)
						digui = self.digui_part2(weizhi_21 + 1, train4, i, test4, list(), list())

						jieguo = 0
						if digui[0] == 1:
							for dg in digui[1]:
								jieguo = jieguo + len(dg)
						if final < jieguo:
							final = jieguo
							zi_result[0] = digui[1]
							zi_result[1] = digui[2]

					for zr0 in zi_result[0]:
						ls1.append(zr0)
					for zr1 in zi_result[1]:
						ls2.append(zr1)

		'''
		weizhi_2 = 0
		weizhi_21 = 0
		weizhi_22 = 0
		zi_ls1 = []
		zi_ls2 = []
		biaozhi = 0
		
		for j in range(weizhi2, len(test4)-1):
			if [test4[j], test4[j + 1]] == [train4[weizhi1], train4[weizhi1 + 1]]:
				weizhi_2 = j+2
				zi_ls1.append(train4[weizhi1])
				zi_ls1.append(train4[weizhi1 + 1])
				zi_ls2.append(weizhi1)
				zi_ls2.append(weizhi1+1)
				break

		#if weizhi_2 < len(test4):
		if weizhi_2 != 0:
			biaozhi = 1
			if weizhi_2 < len(test4):
				for k in range(weizhi_2, len(test4)):
					if weizhi1 + 2 + k - weizhi_2 < len(train4):
						if test4[k] == train4[weizhi1 + k - weizhi_2 + 2]:
							zi_ls1.append(train4[weizhi1 + k - weizhi_2 + 2])
							zi_ls2.append(weizhi1 + k - weizhi_2 + 2)
						else:
							weizhi_21 = weizhi1 + k - weizhi_2 + 2
							weizhi_22 = k
							break
					else:
						break
			ls1.append(zi_ls1)
			ls2.append(zi_ls2)


		if weizhi_22 != 0:
			if weizhi_22 < len(test4) - 1:
				if weizhi_21 + 1 < len(train4) - 1:

					zi_result = [list(), list()]
					final = 0
					for i in range(weizhi_22, len(test4)-1):
						#print("weizhi_22: ", weizhi_22)
						digui = self.seconddigui_part2(weizhi_21+1, train4, i, test4, list(), list())

						jieguo = 0
						if digui[0] == 1:
							for dg in digui[1]:
								jieguo = jieguo + len(dg)
						if final < jieguo:
							final = jieguo
							zi_result[0] = digui[1]
							zi_result[1] = digui[2]

					for zr0 in zi_result[0]:
						ls1.append(zr0)
					for zr1 in zi_result[1]:
						ls2.append(zr1)
		'''
		return [biaozhi, ls1, ls2]


	def seconddigui_part2(self, weizhi1, train4, weizhi2, test4, ls1, ls2):
		weizhi_1 = 0
		weizhi_21 = 0
		weizhi_22 = 0
		zi_ls1 = []
		zi_ls2 = []
		biaozhi = 0

		#print("weizhi1:", weizhi1)
		#print("len(train4):", len(train4))
		#print("weizhi2:", weizhi2)
		#print("len(test4):", len(test4))
		for j in range(weizhi1, len(train4) - 1):
			if [test4[weizhi2], test4[weizhi2+1]] == [train4[j], train4[j+1]]:
				weizhi_1 = j + 2
				zi_ls1.append(train4[j])
				zi_ls1.append(train4[j + 1])
				zi_ls2.append(j)
				zi_ls2.append(j + 1)
				break

		if weizhi_1 != 0:
			biaozhi = 1
			if weizhi_1 < len(train4):
				for k in range(weizhi_1, len(train4)):
					if weizhi2 + 2 + k - weizhi_1 < len(test4):
						if train4[k] == test4[weizhi2 + 2 + k - weizhi_1]:
							zi_ls1.append(train4[k])
							zi_ls2.append(k)
						else:
							weizhi_21 = k
							weizhi_22 = weizhi2 + 2 + k - weizhi_1
							break
					else:
						break
			ls1.append(zi_ls1)
			ls2.append(zi_ls2)

		if weizhi_21 != 0:
			if weizhi_21 + 1 < len(train4) - 1:
				if weizhi_22 < len(test4) - 1:

					zi_result = [list(), list()]
					final = 0
					for i in range(weizhi_22, len(test4) - 1):
						# print("weizhi_22: ", weizhi_22)
						digui = self.seconddigui_part2(weizhi_21 + 1, train4, i, test4, list(), list())

						jieguo = 0
						if digui[0] == 1:
							for dg in digui[1]:
								jieguo = jieguo + len(dg)
						if final < jieguo:
							final = jieguo
							zi_result[0] = digui[1]
							zi_result[1] = digui[2]

					for zr0 in zi_result[0]:
						ls1.append(zr0)
					for zr1 in zi_result[1]:
						ls2.append(zr1)

		return [biaozhi, ls1, ls2]





	def part3(self, train4, train5, test5, ls2_3, ls51):
		#test5, train5已经-1并split过
		result = [0, list(), list(), list()]
		final = 0

		for i in range(len(test5)):
			ls = self.digui_part3(0, train5, i, test5, list(), list())
			jieguo = 0
			if ls[0] == 1:
				jieguo = len(ls[1])
			if final < jieguo:
				final = jieguo
				result[0] = final
				result[1] = ls[1]
				result[2] = ls[2]

		'''
		for i in range(len(train5)):
			ls = self.digui_part3(i, train5, 0, test5, list(), list())
			jieguo = 0
			if ls[0] == 1:
				jieguo = len(ls[1])
			if final < jieguo:
				final = jieguo
				result[0] = final
				result[1] = ls[1]
				result[2] = ls[2]
		'''
		final = final / len(train5)
		result[0] = final

		print("result[1]: ", result[1])
		print("train5: ", train5)

		ls = []
		for i in range(len(result[2])):
			ls.append(0)

		ls_range = []
		for i in range(len(result[2])):
			ls_range.append(i)

		for j in range(len(result[2])):
			for r3 in ls2_3:
				if r3 == result[2][j]:
					if int(ls51[0]) == result[2][j]:
						ls[j] = 1
						ls_range.remove(j)
						break
					else:
						ls[j] = 3
						ls_range.remove(j)
						break

		for lr in ls_range:
			ls_qian = []
			ls_hou = []

			for i in range(result[2][lr] - 1, -1, -1):
				panduan = 0
				for r3 in ls2_3:
					if r3 == i:
						if int(ls51[0]) == i:
							ls_qian.append([i, 2])
							panduan = 1
							break
						else:
							ls_qian.append([i, 0])
							panduan = 1
							break
				if panduan == 1:
					break

			for i in range(result[2][lr] + 1, len(train4)):
				panduan = 0
				for r3 in ls2_3:
					if r3 == i:
						if int(ls51[0]) == i:
							ls_hou.append([i, 2])
							panduan = 1
							break
						else:
							ls_hou.append([i, 0])
							panduan = 1
							break
				if panduan == 1:
					break

			if len(ls_qian) > 0 and len(ls_hou) > 0:
				if result[2][lr] - ls_qian[0][0] > ls_hou[0][0] - result[2][lr]:
					ls[lr] = ls_hou[0][1]
				else:
					ls[lr] = ls_qian[0][1]

			if len(ls_qian) > 0 and len(ls_hou) == 0:
				ls[lr] = ls_qian[0][1]

			if len(ls_qian) == 0 and len(ls_hou) > 0:
				ls[lr] = ls_hou[0][1]

		result[3] = ls

		return result



	def digui_part3(self, weizhi1, train4, weizhi2, test4, ls1, ls2):
		# test4, train4已经-1并split过
		weizhi_1 = 0
		weizhi_21 = 0
		weizhi_22 = 0
		biaozhi = 0

		for j in range(weizhi1, len(train4)):
			word_sim = self.hownet_dict_advanced.calculate_word_similarity(train4[j], test4[weizhi2])
			if word_sim > 0.73:
				weizhi_1 = j + 1
				ls1.append(train4[j])
				ls2.append(j)
				break

		if weizhi_1 != 0:
			biaozhi = 1
			if weizhi_1 < len(train4):
				for k in range(weizhi_1, len(train4)):
					if weizhi2 + 1 + k - weizhi_1 < len(test4):
						word_sim = self.hownet_dict_advanced.calculate_word_similarity(train4[k], test4[weizhi2 + 1 + k - weizhi_1])
						if word_sim > 0.73:
							ls1.append(train4[k])
							ls2.append(k)
						else:
							weizhi_21 = k
							weizhi_22 = weizhi2 + 1 + k - weizhi_1
							break
					else:
						break

		if weizhi_21 != 0:
			if weizhi_21 + 1 < len(train4):
				if weizhi_22 < len(test4):

					zi_result = [list(), list()]
					final = 0
					for i in range(weizhi_22, len(test4)):
						digui = self.digui_part3(weizhi_21 + 1, train4, i, test4, list(), list())

						jieguo = 0
						if digui[0] == 1:
							jieguo = len(digui[1])
						if final < jieguo:
							final = jieguo
							zi_result[0] = digui[1]
							zi_result[1] = digui[2]

					for zr0 in zi_result[0]:
						ls1.append(zr0)
					for zr1 in zi_result[1]:
						ls2.append(zr1)
		'''
		weizhi_2 = 0
		biaozhi = 0
		weizhi_21 = 0
		weizhi_22 =0

		for i in range(weizhi2, len(test5)):
			word_sim = self.hownet_dict_advanced.calculate_word_similarity(train5[weizhi1], test5[i])
			#print(word_sim)
			if word_sim > 0.73:
				#print(train5[weizhi1], test5[i])
				ls1.append(train5[weizhi1])
				ls2.append(weizhi1)
				weizhi_2 = i + 1
				break

		if weizhi_2 != 0:
			biaozhi = 1
			if weizhi_2 < len(test5):
				for k in range(weizhi_2, len(test5)):
					if weizhi1 + 1 + k - weizhi_2 < len(train5):
						word_sim = self.hownet_dict_advanced.calculate_word_similarity(train5[weizhi1 + k - weizhi_2 + 1], test5[k])
						if word_sim > 0.73:
							ls1.append(train5[weizhi1 + k - weizhi_2 + 1])
							ls2.append(weizhi1 + k - weizhi_2 + 1)
						else:
							weizhi_21 = weizhi1 + k - weizhi_2 + 1
							weizhi_22 = k
							break
					else:
						break

		if weizhi_22 != 0:
			if weizhi_22 < len(test5):
				if weizhi_21 + 1 < len(train5):

					zi_result = [list(), list()]
					final = 0
					for i in range(weizhi_22, len(test5)):
						digui = self.seconddigui_part3(weizhi_21 + 1, train5, i, test5, list(), list())

						jieguo = 0
						if digui[0] == 1:
							jieguo = len(digui[1])
						if final < jieguo:
							final = jieguo
							zi_result[0] = digui[1]
							zi_result[1] = digui[2]

					for zr0 in zi_result[0]:
						ls1.append(zr0)
					for zr1 in zi_result[1]:
						ls2.append(zr1)
		'''
		return [biaozhi, ls1, ls2]



	def seconddigui_part3(self, weizhi1, train4, weizhi2, test4, ls1, ls2):
		weizhi_1 = 0
		weizhi_21 = 0
		weizhi_22 = 0
		biaozhi = 0

		for j in range(weizhi1, len(train4)):
			word_sim = self.hownet_dict_advanced.calculate_word_similarity(train4[j], test4[weizhi2])
			if word_sim > 0.73:
				weizhi_1 = j + 1
				ls1.append(train4[j])
				ls2.append(j)
				break

		if weizhi_1 != 0:
			biaozhi = 1
			if weizhi_1 < len(train4):
				for k in range(weizhi_1, len(train4)):
					if weizhi2 + 1 + k - weizhi_1 < len(test4):
						word_sim = self.hownet_dict_advanced.calculate_word_similarity(train4[k], test4[weizhi2 + 1 + k - weizhi_1])
						if word_sim > 0.73:
							ls1.append(train4[k])
							ls2.append(k)
						else:
							weizhi_21 = k
							weizhi_22 = weizhi2 + 1 + k - weizhi_1
							break
					else:
						break

		if weizhi_21 != 0:
			if weizhi_21 + 1 < len(train4):
				if weizhi_22 < len(test4):

					zi_result = [list(), list()]
					final = 0
					for i in range(weizhi_22, len(test5)):
						digui = self.seconddigui_part3(weizhi_21 + 1, train5, i, test5, list(), list())

						jieguo = 0
						if digui[0] == 1:
							jieguo = len(digui[1])
						if final < jieguo:
							final = jieguo
							zi_result[0] = digui[1]
							zi_result[1] = digui[2]

					for zr0 in zi_result[0]:
						ls1.append(zr0)
					for zr1 in zi_result[1]:
						ls2.append(zr1)

		return [biaozhi, ls1, ls2]





	def for_part53(self, test5, ls2_4, ls3_1, ls3_2, ls3_3, ls5_2):

		test_l1 = []
		#print("ls3_1: ", ls3_1)
		for l1 in ls3_1:
			#print("l1: ", l1)
			zi_tl1 = []
			for i in range(len(test5)):
				word_sim = self.hownet_dict_advanced.calculate_word_similarity(l1, test5[i])
				if word_sim > 0.73:
					zi_tl1.append(i)
			test_l1.append(zi_tl1)
		#print("test_l1: ", test_l1)

		#x = 0
		if len(test_l1) > 1:
			ls_hunhe = []
			for i in range(len(test_l1) - 1):
				if i == 0:
					ls_hunhe = test_l1[i]
				ls_hunhe = list(product(ls_hunhe, test_l1[i + 1]))

			new_ls_hunhe = []
			for lh in ls_hunhe:
				self.move_list(lh, new_ls_hunhe)

			jiange = len(ls3_2)
			ls_jiweiyizu = []
			ls = []
			for i in range(len(new_ls_hunhe)):
				if i % jiange == 0:
					if len(ls) > 0:
						ls_jiweiyizu.append(ls)
					ls = []
				ls.append(new_ls_hunhe[i])
				if i == len(new_ls_hunhe) - 1:
					ls_jiweiyizu.append(ls)

			ls_fuheyaoqiu = []
			for l_j in ls_jiweiyizu:
				panduan = 1
				for i in range(len(l_j) - 1):
					if l_j[i] >= l_j[i + 1]:
						panduan = 0
						break
				if panduan == 1:
					ls_fuheyaoqiu.append(l_j)
			# print("ls_fuheyaoqiu: ", ls_fuheyaoqiu)
		else:
			ls_fuheyaoqiu = test_l1

		ls_zong = []
		for lsf in ls_fuheyaoqiu:
			ls = []
			for i in range(len(ls3_2)):
				ls.append(0)
			ls_range = []
			for i in range(len(ls3_2)):
				ls_range.append(i)

			for j in range(len(ls)):
				for l52 in ls5_2:
					panduan = 0
					for r3 in ls2_4:
						#print("r3:", r3)
						#print("lsf:", lsf)
						if r3 == lsf[j]:
							if int(l52) == lsf[j]:
								ls[j] = 1
								ls_range.remove(j)
								panduan = 1
								break
							else:
								ls[j] = 3
								ls_range.remove(j)
								panduan = 1
								break
					if panduan == 1:
						break


			for lr in ls_range:
				result2lr = lsf[lr]
				ls_qian = []
				ls_hou = []

				for i in range(result2lr - 1, -1, -1):
					panduan = 0
					for r3 in ls2_4:
						if r3 == i:
							for l52 in ls5_2:
								if int(l52) == i:
									ls_qian.append([i, 2])
									panduan = 1
									break
								else:
									ls_qian.append([i, 0])
									panduan = 1
									break
					if panduan == 1:
						break

				for i in range(result2lr + 1, len(train4)):
					panduan = 0
					for r3 in ls2_4:
						if r3 == i:
							for l52 in ls5_2:
								if int(l52) == i:
									ls_hou.append([i, 2])
									panduan = 1
									break
								else:
									ls_hou.append([i, 0])
									panduan = 1
									break
					if panduan == 1:
						break

				if len(ls_qian) > 0 and len(ls_hou) > 0:
					if result2lr - ls_qian[0][0] > ls_hou[0][0] - result2lr:
						ls[lr] = ls_hou[0][1]
					else:
						ls[lr] = ls_qian[0][1]

				if len(ls_qian) > 0 and len(ls_hou) == 0:
					ls[lr] = ls_qian[0][1]

				if len(ls_qian) == 0 and len(ls_hou) > 0:
					ls[lr] = ls_hou[0][1]

			ls_zong.append(ls)

		final = 0
		for lz in ls_zong:
			count = 0
			for i in range(len(ls3_3)):
				if ls3_3[i] == lz[i]:
					count = count + 1
			if final < count:
				final = count

		final = final / len(ls3_3)

		'''
			for i in range(len(ls5_1)):
				ls52i = ls5_2[i]
				for ls52 in ls52i:
					for l_j in ls_fuheyaoqiu:
						# 不同的全套组合
						num = 0
						for k in range(len(ls3_2)):
							if int(l_j[k]) != int(ls52):
								guodu = int(ls52) - int(l_j[k]) - ( int(ls5_1[i]) - int(ls3_2[k]) )
								guodu = guodu * guodu
								guodu = guodu ** 0.5
								num = num + guodu  # 系数，可调
						#if num == 0:
							#print("int(ls52): ", int(ls52))
							#print("ls_fuheyaoqiu: ", ls_fuheyaoqiu)
							#print("int(ls5_1[i]): ", int(ls5_1[i]))
							#print("ls3_2: ", ls3_2)
						if x == 0 or x > num:
							x = num
		if len(ls3_2) > 0:
			x = x / len(ls3_2)
			final = 1 - x * x / len(train5)  # 系数，可调
		if final < 0:
			final = 0

		print("final:", final)
		'''
		return final



	def part4(self, train4, test4, ls1, ls2):
		#test5, train5已经-1并split过

		test_l1 = []
		for l1 in ls1:
			zi_tl1 = []
			for i in range(len(test4)-len(l1)):
				pos_zuhe = []
				weizhi_zuhe = []
				for j in range(len(l1)):
					pos_zuhe.append(test4[i+j])
				if pos_zuhe == l1:
					weizhi_zuhe.append(i)
					weizhi_zuhe.append(i+len(l1)-1)
					zi_tl1.append(weizhi_zuhe)
			test_l1.append(zi_tl1)

		ls_hunhe = []
		for i in range(len(test_l1) - 1):
			if i == 0:
				ls_hunhe = test_l1[i]
			ls_hunhe = list(product(ls_hunhe, test_l1[i + 1]))

		new_ls_hunhe = []
		for lh in ls_hunhe:
			self.move_list(lh, new_ls_hunhe)

		jiange = len(ls2)
		ls_jiweiyizu = []
		ls = []
		for i in range(len(new_ls_hunhe)):
			if i % jiange == 0:
				if len(ls) > 0:
					ls_jiweiyizu.append(ls)
				ls = []
			ls.append(new_ls_hunhe[i])
			if i == len(new_ls_hunhe)-1:
				ls_jiweiyizu.append(ls)

		ls_fuheyaoqiu = []
		for l_j in ls_jiweiyizu:
			panduan = 1
			for i in range(len(l_j)-1):
				lji = l_j[i]
				lji1 = l_j[i+1]
				if lji[1] >= lji1[0]:
					panduan = 0
					break
			if panduan == 1:
				ls_fuheyaoqiu.append(l_j)
		#print("ls_fuheyaoqiu: ", ls_fuheyaoqiu)

		x = 0
		for l_j in ls_fuheyaoqiu:
			num = 0
			for i in range(len(ls2)-1):
				ls2_1 = ls2[i+1]
				ls2i = ls2[i]
				lji = l_j[i]
				lji1 = l_j[i + 1]
				guodu = ls2_1[0] - ls2i[len(ls2i)-1] - (lji1[0] - lji[1])
				guodu = guodu * guodu
				guodu = guodu ** 0.5
				num = num + guodu / ((len(ls2_1) + len(ls2i)) / 2 - 1)
			if x == 0 or x > num:
				x = num
		#print("x: ", x)
		if len(ls2) > 1:
			x = x / (len(ls2)-1)
		final = 1 - x*x/len(train4)
		if final < 0:
			final = 0
		return final



	def move_list(self, a, D):
		for i in a:
			if type(i) != tuple:
				D.append(i)
			else:
				self.move_list(i, D)










if __name__ == '__main__':
	ltppar = LtpParser()

	fp1 = pd.read_csv('test1.csv')
	contents = []
	for i in range(len(fp1['category'])):
		contents.append(fp1['category'][i])

	fp2 = pd.read_csv('train_input.csv')
	train_contents = []
	for i in range(len(fp2['category'])):
		train_contents.append(fp2['category'][i])

	label = []
	for content in contents:
		test = content.split("#")
		panduan = 0
		pinjie = ''
		ls_pinjie = []
		for train_content in train_contents:
			train = train_content.split("#")
			p5 = ltppar.part5(test[4], train[4])
			result = ltppar.part1(test, train) + p5[0]
			#result = ltppar.part1(test, train)
			result1 = 0
			result2 = 0
			if result == 3:
				c4 = test[2]
				tc4 = train[2]
				c5 = test[3]
				tc5 = train[3]

				c4 = c4[:-1]
				tc4 = tc4[:-1]
				c5 = c5[:-1]
				tc5 = tc5[:-1]

				test4 = c4.split("_")
				train4 = tc4.split("_")
				test5 = c5.split("_")
				train5 = tc5.split("_")
				if len(train4) > 1 and len(test4) > 1 and len(train5) > 1 and len(test5) > 1:
					#print("train4, test4, train5, test5: ", train4, test4, train5, test5)
					result_p2 = ltppar.part2(train4, test4, p5[1])
					result_p3 = ltppar.part3(train4, train5, test5, result_p2[3], p5[1])
					if len(result_p2[5])>0 and len(result_p3[3]) > 0:
						result1 = result_p2[0] * ltppar.for_part52(test4, result_p2[1], result_p2[2], result_p2[4], result_p2[5], p5[2])
						result2 = result_p3[0] * ltppar.for_part53(test5, result_p2[4], result_p3[1], result_p3[2], result_p3[3], p5[2])
						ls_guodu = [result1+result2, result1, result2, result_p2[0], ltppar.for_part52(test4, result_p2[1], result_p2[2], result_p2[4], result_p2[5], p5[2]), result_p3[0], ltppar.for_part53(test5, result_p2[4], result_p3[1], result_p3[2], result_p3[3], p5[2])]
						if len(ls_pinjie) == 0 or ls_pinjie[0] < ls_guodu[0]:
							ls_pinjie = ls_guodu
						#result1 = result_p2[0]
						#result2 = result_p3[0]
						print("for_part52: ", ltppar.for_part52(test4, result_p2[1], result_p2[2], result_p2[4], result_p2[5], p5[2]))
						print("for_part53: ", ltppar.for_part53(test5, result_p2[4], result_p3[1], result_p3[2], result_p3[3], p5[2]))
						'''
						if result1 >= 0.5 and result2 >= 0.5 and result_p2[0] > 0.6 and result_p3[0] > 0.6 and result1+result2 >= 1.05:
							panduan = 1
							print("train4, test4, train5, test5: ", train4, test4, train5, test5)
							print("result: ", result_p2[0], ltppar.for_part52(test4, result_p2[1], result_p2[2], result_p2[4], result_p2[5], p5[2]), result_p3[0], ltppar.for_part53(test5, result_p2[4], result_p3[1], result_p3[2], result_p3[3], p5[2]) )
							break
						'''
		for lp in ls_pinjie:
			pinjie = pinjie + str(lp) + '_'
		#print(pinjie)
		label.append(pinjie)
		#label.append(panduan)

	fp = pd.read_csv('test1_suoyouliucheng.csv')
	fp = fp.drop(columns=["label"])

	dic = {'label': label}
	data = pd.DataFrame(dic)

	file = [fp, data]
	train = pd.concat(file, axis=1)
	# 0是纵向连，1是横向连
	train = train.dropna(axis=0, how='all')  # 删除空行
	train.to_csv('pingjia1.csv', index=False, encoding='utf-8')




