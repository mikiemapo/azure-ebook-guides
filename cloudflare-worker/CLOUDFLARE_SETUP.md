# Cloudflare KV, D1 & R2 Setup Guide

This guide walks you through setting up the enhanced Cloudflare services for your AZ-104 Study Hub.

## Quick Overview

| Service | Purpose | Free Limit |
|---------|---------|------------|
| KV | Cache CPRS questions (saves OpenAI costs) | 1 GB, 100K reads/day |
| D1 | Sync quiz scores across devices | 5 GB, 5M reads/day |
| R2 | Store Anki deck files | 10 GB, zero egress fees |

---

## Step 1: Create KV Namespace (Caching)

Run in your terminal:
```bash
cd cloudflare-worker
wrangler kv namespace create CPRS_CACHE
```

This outputs something like:
```
⛅️ Creating namespace "CPRS_CACHE"
✅ Success! Created namespace with id "abc123..."

Add the following to your wrangler.toml:
[[kv_namespaces]]
binding = "CPRS_CACHE"
id = "abc123..."
```

**Copy the `id` value and update `wrangler.toml`:**
```toml
[[kv_namespaces]]
binding = "CPRS_CACHE"
id = "YOUR_ACTUAL_ID_HERE"
```

---

## Step 2: Create D1 Database (Score Sync)

### Create the database:
```bash
wrangler d1 create az104-study-db
```

This outputs something like:
```
✅ Successfully created DB 'az104-study-db'

[[d1_databases]]
binding = "DB"
database_name = "az104-study-db"
database_id = "xyz789..."
```

**Copy the `database_id` and update `wrangler.toml`:**
```toml
[[d1_databases]]
binding = "DB"
database_name = "az104-study-db"
database_id = "YOUR_ACTUAL_DATABASE_ID_HERE"
```

### Create the table:
```bash
wrangler d1 execute az104-study-db --file=schema.sql
```

---

## Step 3: Create R2 Bucket (Anki Decks)

```bash
wrangler r2 bucket create az104-anki-decks
```

The R2 bucket doesn't need an ID in wrangler.toml - just the bucket name:
```toml
[[r2_buckets]]
binding = "ANKI_DECKS"
bucket_name = "az104-anki-decks"
```

### Upload Anki decks to R2:
```bash
# Upload a single deck
wrangler r2 object put az104-anki-decks/YourDeck.apkg --file=path/to/YourDeck.apkg

# List uploaded decks
wrangler r2 object list az104-anki-decks
```

---

## Step 4: Deploy Updated Worker

After updating wrangler.toml with your IDs:
```bash
wrangler deploy
```

---

## Step 5: Verify Setup

Visit your Worker URL. You should see:
```json
{
  "status": "AZ-104 Study Hub API",
  "version": "2.0",
  "features": {
    "kvCaching": true,
    "d1Database": true,
    "r2Storage": true
  }
}
```

If any feature shows `false`, double-check the corresponding section in wrangler.toml.

---

## Quick Reference: All Commands

```bash
# KV (caching)
wrangler kv namespace create CPRS_CACHE

# D1 (database)
wrangler d1 create az104-study-db
wrangler d1 execute az104-study-db --file=schema.sql

# R2 (file storage)
wrangler r2 bucket create az104-anki-decks
wrangler r2 object put az104-anki-decks/DeckName.apkg --file=./path/to/deck.apkg

# Deploy
wrangler deploy

# View logs (for debugging)
wrangler tail
```

---

## Troubleshooting

### "KV namespace not found"
- Verify the namespace ID in wrangler.toml matches what `wrangler kv namespace list` shows

### "D1 database not found"
- Verify the database ID in wrangler.toml matches what `wrangler d1 list` shows
- Make sure you ran the schema.sql file

### "R2 bucket not found"
- Verify the bucket name matches exactly (case-sensitive)
- Check bucket exists with `wrangler r2 bucket list`

---

## Cost Summary (Free Tier)

| Service | Daily Free Limit | Your Likely Usage |
|---------|-----------------|-------------------|
| KV reads | 100,000 | ~100-500 |
| KV writes | 1,000 | ~10-50 |
| D1 reads | 5,000,000 | ~100-1,000 |
| D1 writes | 100,000 | ~10-50 |
| R2 storage | 10 GB | ~100 MB (decks) |
| R2 downloads | Unlimited | Free! |

You'll stay well within free limits for personal study use.
