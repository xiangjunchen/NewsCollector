#include "StdAfx.h"
#include "TPVcPython.h"

char* WideChartoAnsi(wchar_t * pWideChar)
{
	if (NULL == pWideChar)
		return NULL;
	char* pAnsi = NULL;
	int needBytes = WideCharToMultiByte(CP_ACP,0,pWideChar,-1, NULL,0, NULL, NULL);
	if (needBytes >0)
	{
		pAnsi = new char[needBytes + 1];
		ZeroMemory(pAnsi, needBytes + 1);
		WideCharToMultiByte(CP_ACP, 0, pWideChar, -1, pAnsi,needBytes, NULL, NULL);
	}
	return pAnsi;
}
wchar_t* MultiByteToWide(char* pMultiChar)
{
	if (!pMultiChar)
		return NULL;
	wchar_t* pWideBuf = NULL;
	int needWideBytes = MultiByteToWideChar(CP_ACP, 0, pMultiChar, -1, NULL, NULL);
	if (needWideBytes >0)
	{
		pWideBuf = new wchar_t[needWideBytes + 1];
		ZeroMemory(pWideBuf, (needWideBytes+1) * sizeof(wchar_t));
		MultiByteToWideChar(CP_ACP, 0, pMultiChar, -1, pWideBuf, needWideBytes);
	}
	return pWideBuf;
}

CTPVcPython::CTPVcPython(void)
{
	// ��ʼ��Python

	// ��ʹ��Pythonϵͳǰ������ʹ��Py_Initialize����

	// ���г�ʼ������������Python���ڽ�ģ�鲢���ϵͳ·

	// ����ģ������·���С��������û�з���ֵ�����ϵͳ

	// �Ƿ��ʼ���ɹ���Ҫʹ��Py_IsInitialized��

	Py_Initialize();

	// ����ʼ���Ƿ�ɹ�

	Py_IsInitialized();

	// ��ӵ�ǰ·��

	// ��������ַ�����ΪPython����ֱ�����У�����

	// ��ʾ�ɹ���-1��ʾ�д����ʱ���������Ϊ�ַ���

	// �����﷨����
	PyRun_SimpleString("import sys");
	PyRun_SimpleString("sys.path.append('./')");

}

CTPVcPython::~CTPVcPython(void)
{
	Py_Finalize();

}

void* CTPVcPython::LoadPythonFile(CString sPlugin)
{
	PyObject* pName = NULL;
	PyObject* pModule =NULL;
	PyObject* pDict = NULL;
	// ������ΪPyPlugin�Ľű�
	pName = PyString_FromString(WideChartoAnsi(sPlugin.GetBuffer()));
	pModule = PyImport_Import(pName);
	if (pModule)
	{
		pDict = PyModule_GetDict(pModule);
		if (pDict)
		{
			return pDict;
		}			
	}
	return NULL;	
}	

void* CTPVcPython::GetFunctionProc(CString sFuntionName,void *pPlugin)
{
	PyObject* pFunc = NULL;
	// �ҳ�������ΪAddMult�ĺ���
	pFunc = PyDict_GetItemString((PyObject*)pPlugin, WideChartoAnsi(sFuntionName.GetBuffer()));
	if (!pFunc || !PyCallable_Check(pFunc))
	{
		return NULL;
	}
	return pFunc;
}

CString CTPVcPython::CollectorFromUrl(CString sUrl)
{
	CString sRe = _T("Failed!");
	PyObject* pPlugin = (PyObject*)LoadPythonFile(_T("singlePageContentGet"));
	if(!pPlugin)	
	{
		sRe = _T("LoadPythonFile Failed!");
		return sRe;
	}
	PyObject* pFunc   = (PyObject*)GetFunctionProc(_T("ParserCommentPage"),pPlugin);
	if(!pFunc)		
	{
		sRe = _T("GetFunctionProc Failed!");
		return sRe;
	}
	char* pRe = NULL;
	PyObject *pyParams = PyTuple_New(1);  
	PyObject *py1 = PyString_FromString(WideChartoAnsi(sUrl.GetBuffer()));  
	//PyObject *py2 = PyString_FromString(WideChartoAnsi(sJc2.GetBuffer()));  
	PyTuple_SetItem(pyParams, 0, py1);  
	//PyTuple_SetItem(pyParams, 1, py2);  
	// ok, call the function    
	PyObject *pyResult = PyObject_CallObject(pFunc, pyParams);  
	if(pyResult)  
	{  
		pRe =PyString_AsString(pyResult);
		sRe = MultiByteToWide(pRe);
		//AfxMessageBox(sRe);
	}
	else
	{
		sRe = _T("PyObject_CallObject Return Failed! ");
	}
	if (pyParams)
		Py_DECREF(pyParams);
	if (pFunc)
		Py_DECREF(pFunc);
	//if(pPlugin)
	//	Py_DECREF(pPlugin);

	return sRe;
}

void* CTPVcPython::ProcPythonDemo()
{
	PyObject* pPlugin = (PyObject*)LoadPythonFile(_T("PyPluginTest"));
	PyObject* pFunc   = (PyObject*)GetFunctionProc(_T("AddMult"),pPlugin);
	
	PyObject* pArgs = NULL;
	PyObject* pRet = NULL;
	pArgs = Py_BuildValue("ii", 12, 14);
	pRet = PyEval_CallObject(pFunc,pArgs);
	int a = 0;
	int b = 0;
	if (pRet && PyArg_ParseTuple(pRet,"ii", &a,&b))
	{
		AfxOutputDebugString(_T("success"));
	}
	if (pArgs)
		Py_DECREF(pArgs);
	if (pFunc)
		Py_DECREF(pFunc);

	// �ҳ�������ΪHelloWorld�ĺ���
	pFunc   = (PyObject*)GetFunctionProc(_T("HelloWorld"),pPlugin);
	CString sJc1 = _T("jc1"),sJc2 = _T("jc2");
	char* pRe;
	CString sRe = _T("");
	PyObject *pyParams = PyTuple_New(1);  
	PyObject *py1 = PyString_FromString(WideChartoAnsi(sJc1.GetBuffer()));  
	//PyObject *py2 = PyString_FromString(WideChartoAnsi(sJc2.GetBuffer()));  
	PyTuple_SetItem(pyParams, 0, py1);  
	//PyTuple_SetItem(pyParams, 1, py2);  
	// ok, call the function    
	PyObject *pyResult = PyObject_CallObject(pFunc, pyParams);  
	if(pyResult)  
	{  
		pRe =PyString_AsString(pyResult);
		sRe = MultiByteToWide(pRe);
		AfxMessageBox(sRe);
	}
	if (pFunc)
		Py_DECREF(pFunc);
	if(pPlugin)
		Py_DECREF(pPlugin);
	return NULL;
}

//Py_BuildValue("")                       None
//
//Py_BuildValue("i",123)                 123
//
//Py_BuildValue("iii",123, 456, 789)     (123, 456, 789)
//
//Py_BuildValue("s","hello")             'hello'
//
//Py_BuildValue("ss","hello", "world")    ('hello', 'world')
//
//Py_BuildValue("s#","hello", 4)         'hell'
//
//Py_BuildValue("()")                     ()
//
//Py_BuildValue("(i)",123)               (123,)
//
//Py_BuildValue("(ii)",123, 456)         (123, 456)
//
//Py_BuildValue("(i,i)",123, 456)        (123, 456)
//
//Py_BuildValue("[i,i]",123, 456)        [123, 456]
//
//Py_BuildValue("{s:i,s:i}",
//
//			  "abc", 123, "def", 456)    {'abc': 123, 'def': 456}
//
//Py_BuildValue("((ii)(ii))(ii)",
//
//			  1, 2, 3, 4, 5, 6)         (((1, 2), (3, 4)), (5, 6))