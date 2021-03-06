
// NewsCollectorDlg.h : header file
//

#pragma once
#include "TPCollectorData.h"

// CNewsCollectorDlg dialog
class CNewsCollectorDlg : public CDialog
{
// Construction
public:
	CNewsCollectorDlg(CWnd* pParent = NULL);	// standard constructor

// Dialog Data
	enum { IDD = IDD_NEWSCOLLECTOR_DIALOG };

	protected:
	virtual void DoDataExchange(CDataExchange* pDX);	// DDX/DDV support


// Implementation
protected:
	HICON m_hIcon;

	// Generated message map functions
	virtual BOOL OnInitDialog();
	afx_msg void OnSysCommand(UINT nID, LPARAM lParam);
	afx_msg void OnPaint();
	afx_msg HCURSOR OnQueryDragIcon();
	DECLARE_MESSAGE_MAP()
public:
	afx_msg void OnBnClickedButton2();

	afx_msg void OnCbnSelchangeComboCollector();
	afx_msg void OnBnClickedButton1();

	CTPCollectorData *pCollectorData;
	afx_msg void OnDestroy();
	afx_msg void OnBnClickedButton3();
};
