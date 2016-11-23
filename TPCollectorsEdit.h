#pragma once


// CTPCollectorsEdit dialog

class CTPCollectorsEdit : public CDialog
{
	DECLARE_DYNAMIC(CTPCollectorsEdit)

public:
	CTPCollectorsEdit(CWnd* pParent = NULL);   // standard constructor
	virtual ~CTPCollectorsEdit();

// Dialog Data
	enum { IDD = IDD_TPCOLLECTORSEDIT };

protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV support

	DECLARE_MESSAGE_MAP()
public:
	virtual BOOL OnInitDialog();
};
