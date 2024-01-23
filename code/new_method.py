import hashlib
import os
import random
import time
from pyltp import Postagger, Segmentor
import re
import pandas as pd
from textblob import TextBlob
import requests

class LtpParser:
	def __init__(self):
		LTP_DIR = "D:\ltp_data_v3.4.0"
		self.segmentor = Segmentor(os.path.join(LTP_DIR, "cws.model"))
		self.postagger = Postagger(os.path.join(LTP_DIR, "pos.model"))



	def dengju_qiefen(self, sentence):
		dengju_result = ['s',0]
		if len(sentence) > 50:
			dengju = list(re.findall(r'.{50}', sentence))
			dengju_result[0] = dengju[0]
			dengju_result[1] = 1
		else:
			dengju_result[0] = sentence
			dengju_result[1] = 0
		return dengju_result



	def anbiaodian_qiefen(self, sentence):
		ls = [sen for sen in re.split(r'[？?！!。,，.；;：:\n\r]', sentence) if sen]
		daishan = str(ls[0])
		sentence = sentence.replace(daishan,"")

		words = list(self.segmentor.segment(sentence))
		postags = list(self.postagger.postag(words))

		if postags[0] == 'wp':
			sentence_zuizhong = ''
			for i in range(1, len(words)):
				sentence_zuizhong = sentence_zuizhong + words[i]
			sentence = sentence_zuizhong
		return sentence



	def ni_nin_v(self, sentence):
		words = list(self.segmentor.segment(sentence))
		postags = list(self.postagger.postag(words))
		result = [0, list()]

		ls_p = []
		ls_w = []
		for i in range(len(words)):
			if postags[i] == 'c' or postags[i] == 'd' or postags[i] == 'a' or postags[i] == 'b' or postags[i] == 'r' or postags[i] == 'v' or postags[i] == 'i' or postags[i] == 'u' or postags[i] == 'nt' or postags[i] == 'nd' or postags[i] == 'p':
				ls_p.append(postags[i])
				ls_w.append(words[i])

		for i in range(len(ls_p)):
			if '你' in ls_w[i] or '您' in ls_w[i]:
				result[0] = 1
				result[1].append(['ni', str(i)])

			if '咱' in ls_w[i] or '我们' in ls_w[i]:
				result[0] = 1
				result[1].append(['zan', str(i)])
		'''
		ni_nin = 0
		for word in words:
			if '你' in word or '您' in word or '咱' in word or '我们' in word:
				ni_nin = ni_nin + 1
				
		ni_v = 0
		for i in range(len(postags)-3):
			if postags[i] == 'wp':
				if '你' in words[i+1] or '您' in words[i+1] or '咱' in words[i+1] or '我们' in words[i+1]:
					if postags[i+2] == 'v':
						if postags[i+3] != 'd' and postags[i+3] != 'a' and postags[i+3] != 'u':
							ni_v = ni_v + 1
		if len(words)>2:
			if '你' in words[0] or '您' in words[0] or '咱' in words[0] or '我们' in words[0]:
				if postags[1] == 'v':
					if postags[2] != 'd' and postags[2] != 'a' and postags[2] != 'u':
						ni_v = ni_v + 1

		if ni_v != ni_nin:
			result = 1
		'''

		return result



	def cixing_zuhe(self, sentence):
		result = [0, list()]
		lunci1 = 1
		for i in range(5):
			first_panduan = self.yilun_pinggu(0, sentence, lunci1)
			lunci1 = lunci1 + 1
			lunci2 = 1
			while first_panduan[0] == 1:
				if lunci2 > 5:
					break
				second_panduan = self.yilun_pinggu(first_panduan[1], sentence, lunci2)
				lunci2 = lunci2 + 1
				if second_panduan[0] == 1:
					result[0] = 1
					zi_result = []
					zi_result.append(first_panduan[2])
					zi_result.append(second_panduan[2])
					result[1].append(zi_result)

		return result



	def yilun_pinggu(self, weizhi, sentence, lunci):
		result = [int(0), int(0), list()]
		words = list(self.segmentor.segment(sentence))
		postags = list(self.postagger.postag(words))

		cishu = 0
		cixing_and_xiangyingweizhi = []
		for ceshi in range(1):
			if lunci == 1:
				#cr
				guodu3 = []
				for i in range(weizhi, len(postags)-1):
					if postags[i] == 'c':
						if postags[i+1] == 'r':
							zi_guodu1 = [i, "c"]
							guodu3.append(zi_guodu1)
							zi_guodu2 = [i+1, "r"]
							guodu3.append(zi_guodu2)
							cishu = 1
							weizhi = i + 2
					if cishu == 1:
						break
				if cishu == 1:
					for gd in guodu3:
						cixing_and_xiangyingweizhi.append(gd)
					break
				#c＋v
				guodu4 = []
				cishu_cv = 0
				for i in range(weizhi, len(postags)):
					if postags[i] == 'c':
						zi_guodu1 = [i, "c"]
						guodu4.append(zi_guodu1)
						cishu_cv = 1
					if cishu_cv == 1:
						if postags[i] == 'v' or postags[i] == 'i':
							zi_guodu2 = [i, "v"]
							guodu4.append(zi_guodu2)
							cishu = 1
							weizhi = i + 1
					if cishu == 1:
						break
				if cishu == 1:
					for gd in guodu4:
						cixing_and_xiangyingweizhi.append(gd)
					break
			if lunci == 2:
				#d(a/v)
				guodu1 = []
				for i in range(weizhi, len(postags)-1):
					if postags[i] == 'd' or postags[i] == 'a':
						if postags[i+1] == 'a' or postags[i+1] == 'd':
							zi_guodu1 = [i, "d"]
							guodu1.append(zi_guodu1)
							zi_guodu2 = [i+1, "a"]
							guodu1.append(zi_guodu2)
							cishu = 1
							weizhi = i + 2
						if postags[i + 1] == 'v' or postags[i + 1] == 'i':
							zi_guodu1 = [i, "d"]
							guodu1.append(zi_guodu1)
							zi_guodu2 = [i + 1, "v"]
							guodu1.append(zi_guodu2)
							cishu = 1
							weizhi = i + 2
						if postags[i + 1] == 'p':
							for j in range(i + 2, len(postags)):
								if postags[j] == 'v' or postags[j] == 'i':
									zi_guodu1 = [i, "d"]
									guodu1.append(zi_guodu1)
									zi_guodu2 = [i + 1, "v"]
									guodu1.append(zi_guodu2)
									cishu = 1
									weizhi = j + 1
					if cishu == 1:
						break
				if cishu == 1:
					for gd in guodu1:
						cixing_and_xiangyingweizhi.append(gd)
					break
				# d+r
				guodu7 = []
				cishu_dr = 0
				for i in range(weizhi, len(postags)):
					if postags[i] == 'd' or postags[i] == 'a':
						zi_guodu1 = [i, "d"]
						guodu7.append(zi_guodu1)
						cishu_dr = 1
					if cishu_dr == 1:
						if postags[i] == 'r':
							zi_guodu2 = [i, "r"]
							guodu7.append(zi_guodu2)
							weizhi = i + 1
							cishu = 1
							break
				if cishu == 1:
					for gd in guodu7:
						cixing_and_xiangyingweizhi.append(gd)
					break

			if lunci == 3:
				#r and nt/p
				guodu8 = []
				cishu_rnt1 = 0
				cishu_rnt2 = 0
				weizhi1 = 0
				weizhi2 = 0
				zi_guodu1 = [int(0), ""]
				zi_guodu2 = [int(0), ""]
				for i in range(weizhi, len(postags)):
					if postags[i] == 'r':
						zi_guodu1 = [i, "r"]
						weizhi1 = i+1
						cishu_rnt1 = 1
					if postags[i] == 'nt' or postags[i] == 'nd':
						zi_guodu2 = [i, "n"]
						weizhi2 = i + 1
						cishu_rnt2 = 1
					if postags[i] == 'p':
						zi_guodu2 = [i, "p"]
						weizhi2 = i + 1
						cishu_rnt2 = 1
					if cishu_rnt1 == 1 and cishu_rnt2 == 1:
						cishu = 1
						weizhi = max(weizhi1, weizhi2)
						if weizhi1 < weizhi2:
							guodu8.append(zi_guodu1)
							guodu8.append(zi_guodu2)
						else:
							guodu8.append(zi_guodu2)
							guodu8.append(zi_guodu1)
						break
				if cishu == 1:
					for gd in guodu8:
						cixing_and_xiangyingweizhi.append(gd)
					break

			if lunci == 4:
				#r(v/a/d)
				guodu2 = []
				for i in range(weizhi, len(postags)-1):
					if postags[i] == 'r':
						if postags[i+1] == 'd':
							zi_guodu1 = [i, "r"]
							guodu2.append(zi_guodu1)
							zi_guodu2 = [i+1, "d"]
							guodu2.append(zi_guodu2)
							cishu = 1
							weizhi = i + 2
						if postags[i + 1] == 'a':
							zi_guodu1 = [i, "r"]
							guodu2.append(zi_guodu1)
							zi_guodu2 = [i+1, "a"]
							guodu2.append(zi_guodu2)
							cishu = 1
							weizhi = i + 2
						if postags[i + 1] == 'v' or postags[i + 1] == 'i':
							zi_guodu1 = [i, "r"]
							guodu2.append(zi_guodu1)
							zi_guodu2 = [i + 1, "v"]
							guodu2.append(zi_guodu2)
							cishu = 1
							weizhi = i + 2
						if postags[i + 1] == 'p':
							for j in range(i + 2, len(postags)):
								if postags[j] == 'v' or postags[j] == 'i':
									zi_guodu1 = [i, "r"]
									guodu2.append(zi_guodu1)
									zi_guodu2 = [i + 1, "v"]
									guodu2.append(zi_guodu2)
									cishu = 1
									weizhi = j + 1
									break
					if cishu == 1:
						break
				if cishu == 1:
					for gd in guodu2:
						cixing_and_xiangyingweizhi.append(gd)
					break
			if lunci == 5:
				#vuv
				guodu5 = []
				for i in range(weizhi, len(postags) - 2):
					if postags[i] == 'v' and postags[i+1] == 'u' and postags[i+2] == 'v':
						zi_guodu1 = [i, "v"]
						guodu5.append(zi_guodu1)
						zi_guodu2 = [i+1, "u"]
						guodu5.append(zi_guodu2)
						zi_guodu3 = [i+2, "v"]
						guodu5.append(zi_guodu3)
						weizhi = i + 3
						cishu = 1
						break
				if cishu == 1:
					for gd in guodu5:
						cixing_and_xiangyingweizhi.append(gd)
					break
				#vv
				guodu6 = []
				for i in range(weizhi, len(postags)-1):
					if postags[i] == 'v':
						if postags[i+1] == 'v' or postags[i+1] == 'i':
							zi_guodu1 = [i, "v"]
							guodu6.append(zi_guodu1)
							zi_guodu2 = [i + 1, "v"]
							guodu6.append(zi_guodu2)
							cishu = 1
							weizhi = i + 2
						if postags[i + 1] == 'p':
							for j in range(i + 2, len(postags)):
								if postags[j] == 'v' or postags[j] == 'i':
									zi_guodu1 = [i, "v"]
									guodu6.append(zi_guodu1)
									zi_guodu2 = [i + 1, "v"]
									guodu6.append(zi_guodu2)
									cishu = 1
									weizhi = j + 1
									break
					if cishu == 1:
						break
				if cishu == 1:
					for gd in guodu6:
						cixing_and_xiangyingweizhi.append(gd)
					break
		result[0] = cishu
		result[1] = weizhi
		result[2] = cixing_and_xiangyingweizhi

		return result


	'''
	def yuyi(self, content, cx1i):
		result = []
		words = list(self.segmentor.segment(content))
		ls_key = ["但", "可", "否则", "不然", "恐怕", "而", "唯一", "不", "特", "别", "永", "甭", "没", "无", "什么", "啥", "咋", "怎", "哪", "如", "若", "只", "非", "万一", "一旦", "再", "还", "仅", "即使", "即便", "要", "这么", "那么", "如此", "太", "真", "很", "最", "实", "更", "总", "全", "完", "着", "干脆", "竟", "居然", "多", "反正", "才", "会", "就", "都", "又", "既" "已", "本", "专", "理应", "该", "得", "定", "必", "是", "除", "千万"]
		for i in range(2):
			cxi = cx1i[i]		#first 和 second
			zi_result = []
			for ci in cxi:
				i = ci[0]
				panduan = 0
				for key in ls_key:
					if key in words[i]:
						zi_result.append(words[i])
						panduan = 1
						break
				if panduan == 0:
					zi_result.append(" ")
			result.append(zi_result)
		return result
	'''


	def pos_yuyi(self, sentence):
		result = [list(), list()]
		words = list(self.segmentor.segment(sentence))
		postags = list(self.postagger.postag(words))
		ls_key = ["但", "可", "否则", "然", "而", "竟", "能", '迟早', "不", "唯", "特", "别", "甭", "没", "无", "什么", "啥", "咋", "怎", "哪", "如", "若", "只", "非", "万一", "一旦", "再", "还", "仅", "即", "要", "实", "更", "总", "多", "有", "全", "完", "着", "干脆", "反正", "才", "会", "就", "都", "又", "既" "已", "本", "专", "应", "该", "得", "定", "必", "是", "除", "于", "因", "为", "所", "千万"]
		for i in range(len(words)):
			if postags[i] == 'c' or postags[i] == 'd' or postags[i] == 'a' or postags[i] == 'b' or postags[i] == 'r' or postags[i] == 'v' or postags[i] == 'i' or postags[i] == 'u' or postags[i] == 'nt' or postags[i] == 'nd' or postags[i] == 'p':
				result[0].append(postags[i])
				for key in ls_key:
					if key in words[i]:
						result[1].append(words[i])
						break
		return result



	def yuyi_cixing(self, cx1i, po_yu, ni_zhouwei):
		result = ""

		for i in range(2):
			cxi = cx1i[i] #first or second
			#yui = yuy[i]
			for ci in cxi:
				result = result + ci[1] + '_'
			result = result + '#'
			#for yu in yui:
				#result = result + yu + '_'
			#result = result + '#'

		for i in range(2):
			pyi = po_yu[i]
			for piyi in pyi:
				result = result + piyi + '_'
			result = result + '#'

		for n_z in ni_zhouwei:
			for nz in n_z:
				result = result + nz + '_'
			result = result + '$'

		return result






	def test_cixing_zuhe(self, sentence):
		result = [0, list()]
		lunci1 = 1
		for i in range(5):
			first_panduan = self.test_yilun_pinggu(0, sentence, lunci1)
			lunci1 = lunci1 + 1
			lunci2 = 1
			while first_panduan[0] == 1:
				if lunci2 > 5:
					break
				second_panduan = self.test_yilun_pinggu(first_panduan[1], sentence, lunci2)
				lunci2 = lunci2 + 1
				if second_panduan[0] == 1:
					result[0] = 1
					zi_result = []
					zi_result.append(first_panduan[2])
					zi_result.append(second_panduan[2])
					result[1].append(zi_result)

		return result



	def test_yilun_pinggu(self, weizhi, sentence, lunci):
		result = [int(0), int(0), list()]
		words = list(self.segmentor.segment(sentence))
		postags = list(self.postagger.postag(words))

		cishu = 0
		cixing_and_xiangyingweizhi = []
		for ceshi in range(1):
			if lunci == 1:
				#cr
				guodu3 = []
				for i in range(weizhi, len(postags)-1):
					if postags[i] == 'c':
						if postags[i+1] == 'r':
							zi_guodu1 = [i, "c"]
							guodu3.append(zi_guodu1)
							zi_guodu2 = [i+1, "r"]
							guodu3.append(zi_guodu2)
							cishu = 1
							weizhi = i + 2
					if cishu == 1:
						break
				if cishu == 1:
					for gd in guodu3:
						cixing_and_xiangyingweizhi.append(gd)
					break
				#c＋v
				guodu4 = []
				cishu_cv = 0
				for i in range(weizhi, len(postags)):
					if postags[i] == 'c':
						zi_guodu1 = [i, "c"]
						guodu4.append(zi_guodu1)
						cishu_cv = 1
					if cishu_cv == 1:
						if postags[i] == 'v' or postags[i] == 'i':
							zi_guodu2 = [i, "v"]
							guodu4.append(zi_guodu2)
							cishu = 1
							weizhi = i + 1
					if cishu == 1:
						break
				if cishu == 1:
					for gd in guodu4:
						cixing_and_xiangyingweizhi.append(gd)
					break
			if lunci == 2:
				#d(a/v)
				guodu1 = []
				for i in range(weizhi, len(postags)-1):
					if postags[i] == 'd' or postags[i] == 'a':
						if postags[i+1] == 'a' or postags[i+1] == 'd':
							zi_guodu1 = [i, "d"]
							guodu1.append(zi_guodu1)
							zi_guodu2 = [i+1, "a"]
							guodu1.append(zi_guodu2)
							cishu = 1
							weizhi = i + 2
						if postags[i + 1] == 'v' or postags[i + 1] == 'i':
							zi_guodu1 = [i, "d"]
							guodu1.append(zi_guodu1)
							zi_guodu2 = [i + 1, "v"]
							guodu1.append(zi_guodu2)
							cishu = 1
							weizhi = i + 2
						if postags[i + 1] == 'p':
							for j in range(i + 2, len(postags)):
								if postags[j] == 'v' or postags[j] == 'i':
									zi_guodu1 = [i, "d"]
									guodu1.append(zi_guodu1)
									zi_guodu2 = [i + 1, "v"]
									guodu1.append(zi_guodu2)
									cishu = 1
									weizhi = j + 1
									break
					if cishu == 1:
						break
				if cishu == 1:
					for gd in guodu1:
						cixing_and_xiangyingweizhi.append(gd)
					break
				# d+r
				guodu7 = []
				cishu_dr = 0
				for i in range(weizhi, len(postags)):
					if postags[i] == 'd' or postags[i] == 'a':
						zi_guodu1 = [i, "d"]
						guodu7.append(zi_guodu1)
						cishu_dr = 1
					if cishu_dr == 1:
						if postags[i] == 'r':
							zi_guodu2 = [i, "r"]
							guodu7.append(zi_guodu2)
							weizhi = i + 1
							cishu = 1
							break
				if cishu == 1:
					for gd in guodu7:
						cixing_and_xiangyingweizhi.append(gd)
					break

			if lunci == 3:
				#r and nt/p
				guodu8 = []
				cishu_rnt1 = 0
				cishu_rnt2 = 0
				weizhi1 = 0
				weizhi2 = 0
				zi_guodu1 = [int(0), ""]
				zi_guodu2 = [int(0), ""]
				for i in range(weizhi, len(postags)):
					if postags[i] == 'r':
						zi_guodu1 = [i, "r"]
						weizhi1 = i+1
						cishu_rnt1 = 1
					if postags[i] == 'nt' or postags[i] == 'nd':
						zi_guodu2 = [i, "n"]
						weizhi2 = i + 1
						cishu_rnt2 = 1
					if postags[i] == 'p':
						zi_guodu2 = [i, "p"]
						weizhi2 = i + 1
						cishu_rnt2 = 1
					if cishu_rnt1 == 1 and cishu_rnt2 == 1:
						cishu = 1
						weizhi = max(weizhi1, weizhi2)
						if weizhi1 < weizhi2:
							guodu8.append(zi_guodu1)
							guodu8.append(zi_guodu2)
						else:
							guodu8.append(zi_guodu2)
							guodu8.append(zi_guodu1)
						break
				if cishu == 1:
					for gd in guodu8:
						cixing_and_xiangyingweizhi.append(gd)
					break

			if lunci == 4:
				#r(v/a/d)
				guodu2 = []
				for i in range(weizhi, len(postags)-1):
					if postags[i] == 'r':
						if postags[i+1] == 'd':
							zi_guodu1 = [i, "r"]
							guodu2.append(zi_guodu1)
							zi_guodu2 = [i+1, "d"]
							guodu2.append(zi_guodu2)
							cishu = 1
							weizhi = i + 2
						if postags[i + 1] == 'a':
							zi_guodu1 = [i, "r"]
							guodu2.append(zi_guodu1)
							zi_guodu2 = [i+1, "a"]
							guodu2.append(zi_guodu2)
							cishu = 1
							weizhi = i + 2
						if postags[i + 1] == 'v' or postags[i + 1] == 'i':
							zi_guodu1 = [i, "r"]
							guodu2.append(zi_guodu1)
							zi_guodu2 = [i + 1, "v"]
							guodu2.append(zi_guodu2)
							cishu = 1
							weizhi = i + 2
						if postags[i + 1] == 'p':
							for j in range(i + 2, len(postags)):
								if postags[j] == 'v' or postags[j] == 'i':
									zi_guodu1 = [i, "r"]
									guodu2.append(zi_guodu1)
									zi_guodu2 = [i + 1, "v"]
									guodu2.append(zi_guodu2)
									cishu = 1
									weizhi = j + 1
									break
					if cishu == 1:
						break
				if cishu == 1:
					for gd in guodu2:
						cixing_and_xiangyingweizhi.append(gd)
					break
			if lunci == 5:
				#vuv
				guodu5 = []
				for i in range(weizhi, len(postags) - 2):
					if postags[i] == 'v' and postags[i+1] == 'u' and postags[i+2] == 'v':
						zi_guodu1 = [i, "v"]
						guodu5.append(zi_guodu1)
						zi_guodu2 = [i+1, "u"]
						guodu5.append(zi_guodu2)
						zi_guodu3 = [i+2, "v"]
						guodu5.append(zi_guodu3)
						weizhi = i + 3
						cishu = 1
						break
				if cishu == 1:
					for gd in guodu5:
						cixing_and_xiangyingweizhi.append(gd)
					break
				#vv
				guodu6 = []
				for i in range(weizhi, len(postags)-1):
					if postags[i] == 'v':
						if postags[i+1] == 'v' or postags[i+1] == 'i':
							zi_guodu1 = [i, "v"]
							guodu6.append(zi_guodu1)
							zi_guodu2 = [i + 1, "v"]
							guodu6.append(zi_guodu2)
							cishu = 1
							weizhi = i + 2
						if postags[i + 1] == 'p':
							for j in range(i + 2, len(postags)):
								if postags[j] == 'v' or postags[j] == 'i':
									zi_guodu1 = [i, "v"]
									guodu6.append(zi_guodu1)
									zi_guodu2 = [i + 1, "v"]
									guodu6.append(zi_guodu2)
									cishu = 1
									weizhi = j + 1
									break
					if cishu == 1:
						break
				if cishu == 1:
					for gd in guodu6:
						cixing_and_xiangyingweizhi.append(gd)
					break
		result[0] = cishu
		result[1] = weizhi
		result[2] = cixing_and_xiangyingweizhi

		return result


	'''
	def test_yuyi(self, content, cx1i):
		result = []
		words = list(self.segmentor.segment(content))

		for i in range(2):
			cxi = cx1i[i]		#first 和 second
			zi_result = []
			for ci in cxi:
				i = ci[0]
				zi_result.append(words[i])
			result.append(zi_result)
		return result
	'''



	def test_pos_yuyi(self, sentence):
		result = [list(), list()]
		words = list(self.segmentor.segment(sentence))
		postags = list(self.postagger.postag(words))
		for i in range(len(words)):
			if postags[i] == 'c' or postags[i] == 'd' or postags[i] == 'a' or postags[i] == 'b' or postags[i] == 'r' or postags[i] == 'v' or postags[i] == 'i' or postags[i] == 'u' or postags[i] == 'nt' or postags[i] == 'nd' or postags[i] == 'p':
				result[0].append(postags[i])
				result[1].append(words[i])

		return result



	def test_yuyi_cixing(self, cx1i, po_yu, ni_zhouwei):
		result = ""

		for i in range(2):
			cxi = cx1i[i] #first or second
			#yui = yuy[i]
			for ci in cxi:
				result = result + ci[1] + '_'
			result = result + '#'
			#for yu in yui:
				#result = result + yu + '_'
			#result = result + '#'

		for i in range(2):
			pyi = po_yu[i]
			for piyi in pyi:
				result = result + piyi + '_'
			result = result + '#'

		for n_z in ni_zhouwei:
			for nz in n_z:
				result = result + nz + '_'
			result = result + '$'

		return result



def youdao(text):
	e = text
	timestamp = str(time.time()).replace('.', '')
	lts = str(int(timestamp * 1000))
	salt = lts + str(random.randint(0, 9))
	# md5加密
	sign_str = 'fanyideskweb' + e + salt + 'Ygy_4c=r#e#4EX^NUGUc5'
	sign = hashlib.md5(sign_str.encode(encoding='UTF-8')).hexdigest()
	data = {
        'i': e,
        'from': 'AUTO',
        'to': 'AUTO',
        'smartresult': 'dict',
        'client': 'fanyideskweb',
        'salt': salt,
        'sign': sign,
        'lts': lts,
        'bv': '8485025d8b016004f09679843317d954',
        'doctype': 'json',
        'version': '2.1',
        'keyfrom': 'fanyi.web',
        'action': 'FY_BY_REALTlME'
    }

	url = 'https://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'

	header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/99.0.4844.51 Safari/537.36 Edg/99.0.1150.30",
        'Cookie': 'OUTFOX_SEARCH_USER_ID=-1154806696@10.168.8.76; \
                       OUTFOX_SEARCH_USER_ID_NCOO=1227534676.2988937; \
                       JSESSIONID=aaa7LDLdy4Wbh9ECJb_Vw; ___rl__test__cookies=1563334957868',
        'Referer': 'https://fanyi.youdao.com/'
    }

	response = requests.post(url, data=data, headers=header)
	response.encoding = 'utf-8'
	result = response.json()
	if result['errorCode'] == 0:
		return result['translateResult'][0][0]['tgt']
	else:
		return text



def en_cixing(text):
	result = 0
	blob = TextBlob(text)
	output = str(blob.parse())
	ls_output = output.split(' ')
	#print(ls_output)
	ls_word = []
	ls_cixing = []
	for l_o in ls_output:
		if len(l_o.split('/')) < 2:
			continue
		word = l_o.split('/')[0]
		ls_word.append(word)
		cixing = l_o.split('/')[1]
		ls_cixing.append(cixing)
	print(ls_cixing)
	print(ls_word)
	if len(ls_cixing) > 1:
		# 祈使句
		if ls_cixing[0] == 'VB' or ls_cixing[0] == 'VBP':
			result = 1
		for i in range(len(ls_cixing)-1):
			# 情态动词
			if ls_cixing[i] == 'MD':
				result = 1
				break
			# to do
			if ls_word[i] == 'to':
				if ls_cixing[i + 1] == 'VB' or ls_cixing[i + 1] == 'VBP':
					result = 1
					break
	return result



if __name__ == '__main__':
	ltppar = LtpParser()
	'''
	tents = []
	fp = pd.read_csv('train.csv')
	#fp = fp.loc[:6770]
	for f in fp['category']:
		tents.append(str(f))

	contents = []
	ni_zhouwei = []
	for tent in tents:
		jiance_result = ltppar.ni_nin_v(str(tent))
		# print(str(daice[0]))
		if jiance_result[0] == 1:
			contents.append(str(tent))
			ni_zhouwei.append(jiance_result[1])
	# print(lianxu)

	daixunlian = []
	input = []
	for j in range(len(contents)):
	#content = '你别说真是，老想要喝水，'
		cixing_panduan = ltppar.cixing_zuhe(contents[j])
		if cixing_panduan[0] == 1:
			cx1 = cixing_panduan[1] #所有lunci
			for i in range(len(cixing_panduan[1])):
				daixunlian.append(contents[j])

				cx1i = cx1[i] #每一lunci
				#yuy = ltppar.yuyi(content, cx1i)
				po_yu = ltppar.pos_yuyi(contents[j])

				jiehe = ltppar.yuyi_cixing(cx1i, po_yu, ni_zhouwei[j])
				input.append(jiehe)

	dic_input = {'category': input}
	data_input = pd.DataFrame(dic_input)
	data_input['label'] = 1
	#data_input['label'] = 1
	data_input.to_csv('train_input.csv', index=False, encoding='utf-8')

	dic_daixunlian = {'category': daixunlian}
	data_daixunlian = pd.DataFrame(dic_daixunlian)
	data_daixunlian['label'] = 1
	#data_daixunlian['label'] = 1
	data_daixunlian.to_csv('train_suoyouliucheng.csv', index=False, encoding='utf-8')
	'''

	tents = []
	fp = pd.read_csv('test3_origin.csv')
	# fp = fp.loc[:6770]
	for f in fp['category']:
		tents.append(str(f))

	contents = []
	ni_zhouwei = []
	for i in range(len(tents)):
		lianxu = tents[i]
		while True:
			daice = ltppar.dengju_qiefen(str(lianxu))
			jiance_result = ltppar.ni_nin_v(str(daice[0]))
			if jiance_result[0] == 1:
				contents.append(str(daice[0]))
				#print("daice[0]: ", daice[0])
				ni_zhouwei.append(jiance_result[1])
				#print("jiance_result[1]: ", jiance_result[1])
			if daice[1] == 0:
				break
			lianxu = ltppar.anbiaodian_qiefen(str(lianxu))

	daixunlian = []
	input = []
	for j in range(len(contents)):
		# content = '你别说真是，老想要喝水，'
		cixing_panduan = ltppar.test_cixing_zuhe(contents[j])
		if cixing_panduan[0] == 1:
			cx1 = cixing_panduan[1]  # 所有lunci
			for i in range(len(cixing_panduan[1])):
				daixunlian.append(contents[j])

				cx1i = cx1[i]  # 每一lunci
				#yuy = ltppar.test_yuyi(content, cx1i)
				po_yu = ltppar.test_pos_yuyi(contents[j])

				jiehe = ltppar.test_yuyi_cixing(cx1i, po_yu, ni_zhouwei[j])
				input.append(jiehe)

	dic_input = {'category': input}
	data_input = pd.DataFrame(dic_input)
	data_input['label'] = 0
	# data_input['label'] = 1
	data_input.to_csv('test3.csv', index=False, encoding='utf-8')

	dic_daixunlian = {'category': daixunlian}
	data_daixunlian = pd.DataFrame(dic_daixunlian)
	data_daixunlian['label'] = 0
	# data_daixunlian['label'] = 1
	data_daixunlian.to_csv('test3_suoyouliucheng.csv', index=False, encoding='utf-8')

	'''
	fp = pd.read_csv('test3_origin.csv')
	contents = []
	for f in fp['category']:
		contents.append(str(f))

	daifanyi = []
	for i in range(len(contents)):
		lianxu = contents[i]

		#lianxu = '我一开始不同意，后来我同意了，我连你的这些补习班我都给你找好了，'
		#daifanyi = []

		while True:
			daice = ltppar.dengju_qiefen(str(lianxu))
			jiance_result = ltppar.ni_nin_v(str(daice[0]))
			#print(str(daice[0]))
			if jiance_result == 1:
				daifanyi.append(str(daice[0]))
			if daice[1] == 0:
				break
			lianxu = ltppar.anbiaodian_qiefen(str(lianxu))
			#print(lianxu)
	daixunlian = []
	for dfy in daifanyi:
		print(dfy)
		text = str(youdao(dfy))
		print(text)
		panduan = en_cixing(text)
		if panduan == 1:
			daixunlian.append(dfy)
	print(daixunlian)

	dic_daixunlian = {'category': daixunlian}
	data_daixunlian = pd.DataFrame(dic_daixunlian)
	#data_daixunlian['label'] = 1
	data_daixunlian['label'] = 0
	data_daixunlian.to_csv('test3_fanyiwan.csv', index=False, encoding='utf-8')
	'''