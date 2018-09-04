package src

import (
	"net/http"
	. "github.com/PuerkitoBio/goquery"
)

type Searcher interface {
	GetUrl(name string) string
}

// Baidu Scholar, to find paper's download link
type BaiduSearcher struct {

}

func (self *BaiduSearcher)GetUrl(name string) (*Document, error) {
	res, err := http.Get("http://xueshu.baidu.com/s?wd=paperuri%3A%282c6f7bc4d11b24947097bd4c5131c536%29&filter=sc_long_sign&sc_ks_para=q%3DModelling%20Compression%20with%20Discourse%20Constraints")
	if err != nil { }

	return NewDocumentFromResponse(res)
}


