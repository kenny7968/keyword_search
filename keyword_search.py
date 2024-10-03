import globalPluginHandler
from scriptHandler import script
import api
import ui
import textInfos
from browseMode import BrowseModeDocumentTreeInterceptor
import braille
import speech


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    
    def __init__(self):
        super().__init__()
        self.keywords = {
            "1": "説明",
            "2": "事業所"
            "9": "github"
        }

    @script(
        gesture="kb:NVDA+control+1",
        description="Search for '説明' in the current page",
        category="Keyword Search"
    )
    def script_searchKeyword1(self, gesture):
        self.searchInBrowseMode(self.keywords["1"])

    @script(
        gesture="kb:NVDA+control+2",
        description="Search for '事業所' in the current page",
        category="Keyword Search"
    )
    def script_searchKeyword2(self, gesture):
        self.searchInBrowseMode(self.keywords["2"])

    @script(
        gesture="kb:NVDA+control+9",
        description="Search for 'github' in the current page",
        category="Keyword Search"
    )
    def script_searchKeyword9(self, gesture):
        self.searchInBrowseMode(self.keywords["9"])
    )

    def searchInBrowseMode(self, keyword):
        focus = api.getFocusObject()
        treeInterceptor = focus.treeInterceptor
        if isinstance(treeInterceptor, BrowseModeDocumentTreeInterceptor) and treeInterceptor.isReady:
            try:
                info = treeInterceptor.makeTextInfo(textInfos.POSITION_CARET)
                res = info.find(keyword)
                if res:
                    treeInterceptor.selection = info
                    info.collapse()
                    treeInterceptor.selection = info
                    info.expand(textInfos.UNIT_LINE)
                    ui.message(keyword)
                    braille.handler.handleText(info)
                else:
                    ui.message(f"キーワード '{keyword}' が見つかりません。")
            except e:
                ui.message("検索中にエラーが発生しました。\n" + e)
        else:
            ui.message("ブラウズモードが有効ではありません。")

# アドオンの初期化時に実行される関数
def initialize():
    globalPluginHandler.GlobalPlugin = GlobalPlugin
