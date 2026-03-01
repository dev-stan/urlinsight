export interface Link {
	short_code: string;
	target_url: string;
}

export interface DailyStats {
	date: string;
	clicks: number;
	unique_visitors: number;
}

export interface LinkAnalytics {
	short_code: string;
	target_url: string;
	totals: {
		clicks: number;
		unique_visitors: number;
	};
	daily: DailyStats[];
}

export interface User {
	id: number;
	email: string;
}

export interface TokenResponse {
	access_token: string;
	token_type: string;
}
