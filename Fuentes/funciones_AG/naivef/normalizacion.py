#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 20:38:57 2017

@author: pablo
"""
import numpy as np

class Normalize:
    def normalize(self, S):
        elements = []
        Sn = []
        
        for s in S:
            elements.extend(s)
        
        self.media = np.mean(elements)
        self.std = np.std(elements)
        
        for s in S:
            sn = []
            for i in range(len(s)):
                sn.append((self.media - s[i]) / self.std)
            Sn.append(sn)
        
        return Sn
    
    
    def desnormalize(self, Sn):
        S = []
        for sn in Sn:
            s = []
            for i in range(len(sn)):
                s.append(self.media - self.std * sn[i])
            S.append(s)
        return S
    

        
if __name__ == '__main__':
    S = [[2,1,2,6],[3,4,6,8]]
    N = Normalize()
    
    print 'series:', S 
    Sn = N.normalize(S)
    print 'normalizadas:', Sn
    Sd = N.desnormalize(Sn)
    print 'desnormalizadas:', Sd
    