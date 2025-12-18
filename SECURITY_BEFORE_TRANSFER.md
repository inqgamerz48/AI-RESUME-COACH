# Security Checklist - Before Transferring Repository

**⚠️ CRITICAL: Follow these steps BEFORE selling or transferring this repository!**

## 🔐 Step-by-Step Security Checklist

### ✅ **STEP 1: Revoke API Keys (MOST CRITICAL)**

#### OpenRouter API Key:
1. **Login:** https://openrouter.ai/keys
2. **Find your key** in the dashboard
3. **Click DELETE/REVOKE** on the key
4. **Confirm** the deletion

**Why?** Anyone with your API key can use your credits and rack up charges!

---

### ✅ **STEP 2: Remove Environment Variables from Render**

If you deployed to Render:

1. **Login:** https://dashboard.render.com
2. **Navigate to** your backend service
3. **Go to** Environment → Environment Variables
4. **Delete** the following variables:
   - `OPENROUTER_API_KEY`
   - `SECRET_KEY` (buyer should generate their own)
   - `DATABASE_URL` (if specific to your account)
5. **Save** changes

Or simply **DELETE the entire Render service** if you won't use it.

---

### ✅ **STEP 3: Clean Local Environment Files**

Delete all local `.env` files that contain secrets:

```bash
# From the project root
rm backend/.env
rm frontend/.env.local  # If it exists
```

**Verify they're deleted:**
```bash
ls -la backend/.env 2>/dev/null && echo "⚠️ Still exists!" || echo "✅ Deleted"
ls -la frontend/.env.local 2>/dev/null && echo "⚠️ Still exists!" || echo "✅ Deleted"
```

---

### ✅ **STEP 4: Verify Git History is Clean**

Check that no actual secrets were committed:

```bash
# Check for API keys in commit history
git log --all -p | grep -E "sk-or-v1-[a-f0-9]{64}" | head -5

# If this shows actual keys (64 character hex), you need to:
# 1. Rewrite git history (advanced - use BFG Repo-Cleaner)
# 2. Or create a fresh repo with clean history
```

**Current Status:** ✅ Only placeholder values found in git history - SAFE!

---

### ✅ **STEP 5: Database Cleanup (If Applicable)**

If using a production database:

1. **Backup** any data the buyer doesn't need
2. **Clear user data** (emails, passwords, personal info)
3. **Delete the database** or transfer ownership to buyer
4. Let buyer create their own database

---

### ✅ **STEP 6: Generate New Secrets Document for Buyer**

Create a `SETUP_INSTRUCTIONS.md` for the buyer:

```markdown
# Setup Instructions

## Required API Keys

You need to obtain the following API keys:

1. **OpenRouter API Key**
   - Get from: https://openrouter.ai/keys
   - Add to: `backend/.env` as `OPENROUTER_API_KEY=your-key`

2. **Secret Key** (for JWT tokens)
   - Generate with: `openssl rand -hex 32`
   - Add to: `backend/.env` as `SECRET_KEY=generated-key`

3. **Database URL**
   - Get from: Neon, Supabase, or any PostgreSQL provider
   - Add to: `backend/.env` as `DATABASE_URL=postgresql://...`

See `.env.example` for complete template.
```

---

## 🎯 **Quick Pre-Transfer Checklist**

Before transferring the repo, verify:

- [ ] **OpenRouter API key REVOKED** at https://openrouter.ai/keys
- [ ] **Render environment variables DELETED** or service removed
- [ ] **Local .env files DELETED** (`backend/.env`, `frontend/.env.local`)
- [ ] **Git history checked** (no actual secrets committed)
- [ ] **Database access REVOKED** or database deleted
- [ ] **New secrets generated** by buyer (don't share yours!)
- [ ] **GitHub repo transferred** to buyer's account

---

## ⚠️ **What Can Go Wrong?**

### **If you forget to revoke API keys:**
- ❌ Buyer can use your OpenRouter credits
- ❌ You'll be charged for their usage
- ❌ Your account could rack up unexpected bills

### **If secrets are in git history:**
- ❌ Anyone cloning the repo gets your secrets
- ❌ Even after deletion, they exist in git history
- ❌ Requires git history rewrite to fix

### **If you share your SECRET_KEY:**
- ❌ Buyer can forge JWT tokens
- ❌ Security compromise for existing users
- ❌ They should generate their own!

---

## 📞 **Emergency - I Already Transferred!**

If you already transferred without revoking:

1. **IMMEDIATELY** login to https://openrouter.ai/keys
2. **REVOKE** the API key NOW
3. **Check billing** at https://openrouter.ai/activity
4. **Contact OpenRouter support** if unauthorized usage occurred
5. **Change passwords** on all related accounts

---

## ✅ **Safe Transfer Summary**

**For You (Seller):**
- Revoke all API keys
- Remove all environment variables from hosting
- Delete local .env files
- Transfer clean repo to buyer

**For Buyer:**
- Generate their own SECRET_KEY
- Obtain their own OPENROUTER_API_KEY
- Create their own database
- Set up their own Render/hosting account

**Both of you should have COMPLETELY SEPARATE:**
- API keys
- Databases
- Hosting accounts
- Environment configurations

---

**Last Updated:** 2025-12-17  
**Your Current API Key (TO BE REVOKED):** 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

⚠️ **Remember:** When in doubt, REVOKE and REGENERATE! Better safe than sorry.
