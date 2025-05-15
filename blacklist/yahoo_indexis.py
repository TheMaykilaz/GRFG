from rest_framework.views import APIView
from rest_framework.response import Response
import yfinance as yf

class IndexDataAPI(APIView):
    def get(self, request):
        symbols = ["SPY", "QQQ", "DIA", "EXS1.DE", "ISF.L"]
        result = []
        for symbol in symbols:
            data = yf.Ticker(symbol)
            info = data.info
            hist = data.history(period="1d")
            try:
                result.append({
                    'symbol': symbol,
                    'name': info.get('longName'),
                    'exchange': info.get('exchange'),
                    'quote_type': info.get('quoteType'),
                    'market_cap': info.get('marketCap'),
                    'open': hist['Open'].iloc[-1],
                    'high': hist['High'].iloc[-1],
                    'low': hist['Low'].iloc[-1],
                    'close': hist['Close'].iloc[-1],
                    'volume': hist['Volume'].iloc[-1],
                })
            except Exception as e:
                continue
        return Response(result)
