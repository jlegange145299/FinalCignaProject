# Deployment Checklist - Cigna AI Assistant

Use this checklist before deploying to production.

## 🔒 Security

- [ ] `.env` file is in `.gitignore` (never commit API keys)
- [ ] `.streamlit/secrets.toml` is in `.gitignore`
- [ ] All API keys are using production credentials (not test keys)
- [ ] D-ID API key has sufficient rate limits for expected traffic
- [ ] OpenAI API key has usage limits configured
- [ ] Remove or disable all `print()` debug statements in production
- [ ] Consider implementing request logging for monitoring

## ⚙️ Configuration

- [ ] `.env` file created with valid D-ID API key
- [ ] `.streamlit/secrets.toml` created with OpenAI credentials
- [ ] OpenAI Assistant is properly trained with latest documents
- [ ] Assistant ID is correct in secrets file
- [ ] Streamlit theme colors match brand guidelines
- [ ] Video avatar image URL is accessible (alice.png)
- [ ] All S3 asset URLs are working and publicly accessible

## 🧪 Testing

- [ ] Run `python setup.py` - all checks pass ✅
- [ ] Basic chat interaction works
- [ ] Multi-turn conversation maintains context
- [ ] Video generation works (D-ID API responds)
- [ ] Video generation failure is handled gracefully
- [ ] Citations display correctly (if knowledge base has them)
- [ ] Sidebar widgets are functional
- [ ] Satisfaction slider works (0-10 range)
- [ ] Contact preference dropdowns work
- [ ] UI displays correctly on desktop browsers
- [ ] UI displays correctly on mobile devices
- [ ] Test with various question lengths
- [ ] Test with very long AI responses (>225 chars)
- [ ] Verify no memory leaks with long sessions

## 📊 Performance

- [ ] OpenAI API response times are acceptable (<10 seconds)
- [ ] D-ID video generation times are acceptable (<30 seconds)
- [ ] Page loads without errors
- [ ] No console errors in browser developer tools
- [ ] Session state management works correctly
- [ ] App doesn't crash with concurrent users (if applicable)

## 📱 Deployment Platform

### Streamlit Cloud
- [ ] Connect GitHub repository
- [ ] Configure secrets in Streamlit Cloud dashboard
- [ ] Set environment variables if needed
- [ ] Test deployment URL
- [ ] Configure custom domain (optional)

### Docker (if using docker-compose.yml)
- [ ] Update docker-compose.yml with correct paths
- [ ] Build Docker image successfully
- [ ] Test container locally
- [ ] Configure environment variables in Docker
- [ ] Set up volume mounts for persistence if needed

### Heroku (if using Procfile)
- [ ] Procfile exists and is configured correctly
- [ ] Add buildpacks for Python
- [ ] Configure Config Vars for all secrets
- [ ] Test on Heroku staging before production
- [ ] Set up monitoring/logging

## 📚 Documentation

- [ ] README.md is up to date
- [ ] QUICKSTART.md tested and accurate
- [ ] API key acquisition instructions are clear
- [ ] Troubleshooting section covers common issues
- [ ] Code comments are sufficient for maintenance

## 🚨 Monitoring & Maintenance

- [ ] Set up error logging/monitoring (Sentry, LogRocket, etc.)
- [ ] Configure alerts for API failures
- [ ] Set up usage tracking for OpenAI API costs
- [ ] Set up usage tracking for D-ID API costs
- [ ] Plan for OpenAI Assistant knowledge base updates
- [ ] Document process for updating Cigna documents
- [ ] Create backup of Assistant configuration
- [ ] Set up scheduled health checks

## 🎯 User Experience

- [ ] Welcome message is clear and helpful
- [ ] Chat placeholder text is appropriate
- [ ] Error messages are user-friendly (not technical)
- [ ] Video loading states are indicated
- [ ] No broken image links
- [ ] Branding is consistent (logo, colors, fonts)
- [ ] Accessibility: keyboard navigation works
- [ ] Accessibility: screen reader compatible (test if required)

## 📈 Analytics (Optional but Recommended)

- [ ] Set up Google Analytics or similar
- [ ] Track common questions asked
- [ ] Track video generation success rate
- [ ] Track satisfaction slider responses
- [ ] Track contact preference selections
- [ ] Monitor session duration
- [ ] Monitor bounce rate

## 🔄 Rollback Plan

- [ ] Document current working version/commit
- [ ] Test rollback procedure
- [ ] Have backup of OpenAI Assistant configuration
- [ ] Know how to quickly disable new features if needed
- [ ] Document manual testing steps for post-rollback verification

## ✅ Final Sign-Off

Before going live:

- [ ] Product owner has approved UI/UX
- [ ] Stakeholders have tested functionality
- [ ] Legal has approved chatbot responses (if required)
- [ ] Compliance has approved data handling (if required)
- [ ] Support team trained on common issues
- [ ] Escalation process documented

---

## Deployment Commands

### Streamlit Cloud
1. Push code to GitHub
2. Go to https://share.streamlit.io/
3. Deploy from repository

### Local/Server Deployment
```bash
# Verify setup
python setup.py

# Run with production config
streamlit run app7.py --server.port 8501 --server.address 0.0.0.0
```

### Docker
```bash
# If using Docker
docker-compose up -d
```

---

## Post-Deployment

- [ ] Verify app is accessible at production URL
- [ ] Test with real user questions
- [ ] Monitor logs for first 24 hours
- [ ] Check API usage/costs after first week
- [ ] Gather user feedback
- [ ] Plan first update based on feedback

---

## Emergency Contacts

Document who to contact if:
- OpenAI API fails: _______________________
- D-ID API fails: _______________________
- Deployment issues: _______________________
- Content/compliance issues: _______________________

---

## Notes

**Date Deployed**: _______________________
**Deployed By**: _______________________
**Version/Commit**: _______________________
**Production URL**: _______________________

---

Good luck with your deployment! 🚀
