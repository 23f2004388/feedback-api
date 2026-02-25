# DevSync Feedback & Code Interpreter API

[![Daily Repository Update](https://github.com/23f2004388/feedback-api/actions/workflows/daily-update.yml/badge.svg)](https://github.com/23f2004388/feedback-api/actions/workflows/daily-update.yml)

## 📌 Project Overview

This repository contains a FastAPI-based backend service built as part of DevSync automation tasks.

The project demonstrates:

- ✅ Sentiment analysis endpoint (`/comment`)
- ✅ Python code execution and error analysis (`/code-interpreter`)
- ✅ Automated daily repository updates using GitHub Actions
- ✅ CI/CD visibility via workflow status badge
- ✅ Scheduled commits for activity tracking and compliance

---

## 🚀 API Endpoints

### 1️⃣ POST `/comment`

Performs sentiment analysis on a given comment.

**Request:**
```json
{
  "comment": "This product is amazing!"
}
