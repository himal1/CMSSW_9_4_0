ifeq ($(strip $(PyFourMuAnalysisUpsilon)),)
PyFourMuAnalysisUpsilon := self/src/FourMuAnalysis/Upsilon/python
src_FourMuAnalysis_Upsilon_python_parent := 
ALL_PYTHON_DIRS += $(patsubst src/%,%,src/FourMuAnalysis/Upsilon/python)
PyFourMuAnalysisUpsilon_files := $(patsubst src/FourMuAnalysis/Upsilon/python/%,%,$(wildcard $(foreach dir,src/FourMuAnalysis/Upsilon/python ,$(foreach ext,$(SRC_FILES_SUFFIXES),$(dir)/*.$(ext)))))
PyFourMuAnalysisUpsilon_LOC_USE := self  
PyFourMuAnalysisUpsilon_PACKAGE := self/src/FourMuAnalysis/Upsilon/python
ALL_PRODS += PyFourMuAnalysisUpsilon
PyFourMuAnalysisUpsilon_INIT_FUNC        += $$(eval $$(call PythonProduct,PyFourMuAnalysisUpsilon,src/FourMuAnalysis/Upsilon/python,src_FourMuAnalysis_Upsilon_python,1,1,$(SCRAMSTORENAME_PYTHON),$(SCRAMSTORENAME_LIB),,))
else
$(eval $(call MultipleWarningMsg,PyFourMuAnalysisUpsilon,src/FourMuAnalysis/Upsilon/python))
endif
ALL_COMMONRULES += src_FourMuAnalysis_Upsilon_python
src_FourMuAnalysis_Upsilon_python_INIT_FUNC += $$(eval $$(call CommonProductRules,src_FourMuAnalysis_Upsilon_python,src/FourMuAnalysis/Upsilon/python,PYTHON))
