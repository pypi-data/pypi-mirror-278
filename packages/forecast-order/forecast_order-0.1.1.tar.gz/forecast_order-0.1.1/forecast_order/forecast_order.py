import requests
import json
import time

class ForecastOrders:

    HAWK_API_URL = "https://dev-api-hawk.rox-jp.com/v1.0"
    # ジョブステータス取得用エンドポイント
    GET_JOBS_STATUS_ENDPOINT = "/pred/jobs/"

    def forecast_orders(self, client_id, api_token, pred_id, original_data,):
        print("forecast_orders")

        self.headers = {"Authorization": f"Bearer {api_token}"}
        # 予測用エンドポイント
        forecast_endpoint = self.create_forecast_endpoint(client_id, pred_id)

        # Hawk APIリクエスト用実績データ
        self.request_body = self.create_body(original_data)

        # 予測計算を開始
        start_forecast_response = self.start_forecast(forecast_endpoint, self.request_body)
        # job_id
        job_id = json.loads(start_forecast_response.text)["job_id"]
        # jobステータス
        job_status = self.get_job_status(job_id)

        # jobステータスがRUNNINGの場合、再度ステータス取得処理
        if job_status == "RUNNING":
            print("Job is running")
            time.sleep(30)
            job_status = self.get_job_status(job_id)

        # 予測結果を取得
        get_forecast_result_response = self.get_forecast_result(forecast_endpoint)

        # JSONデータを辞書型に変換
        forecast_result = json.loads(get_forecast_result_response.text)
        return forecast_result

    # 予測計算エンドポイントを作成する
    def create_forecast_endpoint(self, client_id, pred_id):
        print("create_endpoint")
        return f"/pred/{client_id}/{pred_id}"

    # Hawk API リクエストボディの作成する
    def create_body(self, original_data):
        print("create_body")

        actual_data = [
            {"date": str(data["受注日(YYYYMMDD形式)"]), "value": data["金額"]}
            for data in original_data
        ]

        request_body = [{"spot_id": "test", "loc_zip_code": "test", "actual": actual_data}]

        return request_body


    # 予測計算を開始する
    def start_forecast(self, forecast_endpoint, request_body):
        print("start_forecast")

        request_url = f"{self.HAWK_API_URL}/{forecast_endpoint}"

        response = requests.post(request_url, headers=self.headers, json=request_body)
        # レスポンスのステータスコードを確認
        # print("ステータスコード:", response.status_code)
        # レスポンスの内容を確認
        # print("レスポンスの内容:", response.text)

        return response


    # ジョブの状態を取得する
    def get_job_status(self, job_id):
        print("get_job_status")

        request_url = f"{self.HAWK_API_URL}/{self.GET_JOBS_STATUS_ENDPOINT}/{job_id}"

        response = requests.get(request_url, headers=self.headers)
        response_text = json.loads(response.text)
        job_status = response_text["job_status"]

        return job_status


    # 予測結果を取得する
    def get_forecast_result(self, forecast_endpoint):
        print("get_forecast_result")

        request_url = f"{self.HAWK_API_URL}/{forecast_endpoint}"

        response = requests.get(request_url, headers=self.headers, json=self.request_body)
        # レスポンスのステータスコードを確認
        # print("ステータスコード:", response.status_code)
        # レスポンスの内容を確認
        # print("レスポンスの内容:", response.text)

        return response
