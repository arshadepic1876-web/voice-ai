# Comprehensive Testing & Verification Checklist
## AI Voice-to-Text Task Manager

---

| ID | Test Scenario | Input / Action | Expected Result | Status |
| :--- | :--- | :--- | :--- | :--- |
| **TC01** | Mic Allowed | Click Mic Button & click "Allow" | Recording starts, state changes to `Listening...`, timer ticks | ✅ PASSED |
| **TC02** | Mic Denied | Click Mic Button & click "Block" | Toast error "Microphone permission was denied" appears | ✅ PASSED |
| **TC03** | No Microphone Device | Run browser on system without mic | Toast error "No microphone device was detected" appears | ✅ PASSED |
| **TC04** | Empty Recording | Click Mic & immediately Stop | Backend validation rejects 0-byte audio recording | ✅ PASSED |
| **TC05** | Short Recording | Speak 2 seconds audio clip | Successfully transcribed and parsed | ✅ PASSED |
| **TC06** | Long Recording | Speak until 60 seconds timer cap | Recording auto-stops at 60s limit with toast alert | ✅ PASSED |
| **TC07** | Invalid Audio Format | Upload fake `.txt` file renamed as `.webm` | Backend returns `400 Bad Request` invalid MIME type | ✅ PASSED |
| **TC08** | Large Audio File | Upload >10MB audio file | Backend returns `413 Entity Too Large` error | ✅ PASSED |
| **TC09** | Network Offline | Stop Flask server & click Mic | Toast error "Backend server is offline" displays | ✅ PASSED |
| **TC10** | AWS Credentials Missing | Run without AWS credentials | Seamlessly falls back to local dev transcription mode | ✅ PASSED |
| **TC11** | Speech Recognition | Speak clear sentence | Raw transcript string returned accurately | ✅ PASSED |
| **TC12** | AI Task Parser | Speak "Submit OS project tomorrow" | Parses title "Submit OS project" & resolves due_date | ✅ PASSED |
| **TC13** | Date Resolution | Speak "tomorrow at 5 PM" | Sets `due_date` to tomorrow's date & `due_time` to `"17:00"` | ✅ PASSED |
| **TC14** | Missing Time | Speak "Call Rahul tomorrow" | Defaults `due_time` to `"17:00"` (5:00 PM) | ✅ PASSED |
| **TC15** | Urgent Task | Speak "Urgently buy groceries" | Sets `urgent: true` and displays glowing badge | ✅ PASSED |
| **TC16** | High Priority Task | Speak "Submit report, very important" | Sets `priority: "high"` and displays High badge | ✅ PASSED |
| **TC17** | Normal Task | Speak "Call friend tomorrow" | Sets `priority: "medium"` and `urgent: false` | ✅ PASSED |
| **TC18** | Task Preview Confirmation | Record voice task | Preview Modal opens with pre-filled editable attributes | ✅ PASSED |
| **TC19** | Edit Task before saving | Change title in Preview Modal | Saved task reflects user edited title | ✅ PASSED |
| **TC20** | Complete Task | Click "✓ Complete" on task card | Task title shows strike-through & status updates | ✅ PASSED |
| **TC21** | Delete Task | Click "🗑 Delete" & confirm dialog | Task is deleted from SQLite DB and removed from UI | ✅ PASSED |
| **TC22** | Search Tasks | Type "Python" in search bar | Displays only tasks containing "Python" | ✅ PASSED |
| **TC23** | Filter Tasks | Click "Urgent" filter button | Filters grid to display only urgent tasks | ✅ PASSED |
| **TC24** | Mobile UI Layout | Resize viewport to 375px width | Header stacks, mic button scales, grid becomes 1-column | ✅ PASSED |
| **TC25** | Desktop UI Layout | Open on 1920px display | Grid displays 3 columns with sticky header | ✅ PASSED |
