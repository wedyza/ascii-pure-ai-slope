# Tasks: Video-to-ASCII Player

**Input**: Design documents from `/specs/001-video-to-ascii-player/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Organization**: Tasks grouped by user story for independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3, US4)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project root with server/ and client/ directories
- [x] T002 Initialize server/ Python project with uv (pyproject.toml, .python-version)
- [x] T003 Initialize client/ JavaScript project with npm (package.json)
- [x] T004 [P] Configure ruff + basedpyright in server/pyproject.toml
- [x] T005 [P] Configure .env.example files for server/ and client/
- [x] T006 Create server/src/main.py FastAPI app entry point with CORS middleware

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST complete before ANY user story

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T007 Create Pydantic schemas in server/src/api/schemas.py (VideoUpload, ASCIIConversion, AudioTrack, ErrorResponse)
- [x] T008 Create in-memory storage module in server/src/services/storage.py (dict with TTL-based cleanup)
- [x] T009 Create file validation service in server/src/services/validator.py (format, size, duration checks)
- [x] T010 Create error handling middleware in server/src/api/routes.py (consistent JSON error responses)
- [x] T011 [P] Create client/src/services/api.js (base API client with error handling)

**Checkpoint**: Foundation ready - user story implementation can begin

---

## Phase 3: User Story 1 - Upload and Convert Video (Priority: P1) 🎯 MVP

**Goal**: User can upload a video file and see conversion progress; system converts frames to ASCII

**Independent Test**: Upload a short MP4, verify conversion completes and progress updates

### Implementation for User Story 1

- [x] T012 [US1] Create video-to-ASCII converter in server/src/services/converter.py (pixel-to-character mapping, luminance sampling, @#S%?*+;:,. gradient)
- [x] T013 [US1] Create audio extraction service in server/src/services/audio.py (FFmpeg subprocess for audio stream extraction)
- [x] T014 [US1] Implement POST /upload endpoint in server/src/api/routes.py (accept multipart, validate, start conversion, return UUID)
- [x] T015 [US1] Implement GET /conversion/{id}/status endpoint in server/src/api/routes.py (return status, progress百分比, message)
- [x] T016 [US1] Create client/src/components/UploadForm.jsx (file input, drag-drop, progress bar, error display)
- [x] T017 [US1] Create client/src/pages/Home.jsx (compose UploadForm, wire to API)
- [x] T018 [US1] Add input validation and error messages (400, 413, 422 responses per contracts/api.md)

**Checkpoint**: User can upload video and see conversion complete with progress feedback

---

## Phase 4: User Story 2 - Play ASCII Video with Audio (Priority: P1) 🎯 MVP

**Goal**: User can play the converted ASCII video with synchronized audio and player controls

**Independent Test**: Provide pre-converted ASCII frames, verify playback syncs with audio

### Implementation for User Story 2

- [x] T019 [US2] Implement GET /conversion/{id}/frames endpoint in server/src/api/routes.py (return frames array with frame_rate, width, height, duration)
- [x] T020 [US2] Implement GET /conversion/{id}/audio endpoint in server/src/api/routes.py (stream audio binary with Range request support)
- [x] T021 [US2] Create client/src/components/ASCIIPlayer.jsx (render ASCII frames in pre/canvas element, play/pause/seek/volume controls)
- [x] T022 [US2] Implement audio-ASCII sync logic in client/src/components/ASCIIPlayer.jsx (timestamp alignment between audio playback and frame rendering)
- [x] T023 [US2] Wire ASCIIPlayer into Home.jsx after conversion completes (fetch frames + audio, mount player)

**Checkpoint**: Full upload-to-playback flow works; ASCII video plays with synced audio

---

## Phase 5: User Story 3 - Theme Switching (Priority: P2)

**Goal**: User can toggle dark/light themes with instant visual change and session persistence

**Independent Test**: Toggle theme switch, verify colors change and persist on reload

### Implementation for User Story 3

- [x] T024 [US3] Create client/src/styles/dark.css (CSS custom properties for dark theme)
- [x] T025 [US3] Create client/src/styles/light.css (CSS custom properties for light theme)
- [x] T026 [US3] Create client/src/components/ThemeToggle.jsx (toggle button, localStorage persistence)
- [x] T027 [US3] Wire ThemeToggle into Home.jsx header (apply theme class to html element, load from localStorage on mount)

**Checkpoint**: Theme switching works; dark is default; persists during session

---

## Phase 6: User Story 4 - No Download Capability (Priority: P2)

**Goal**: Converted ASCII content cannot be downloaded by users

**Independent Test**: Inspect page source and network tab; verify no download links or file endpoints

### Implementation for User Story 4

- [x] T028 [US4] Implement DELETE /conversion/{id} endpoint in server/src/api/routes.py (cleanup in-memory data)
- [x] T029 [US4] Add cleanup-on-unload handler in client/src/services/api.js (call DELETE on beforeunload event)
- [x] T030 [US4] Remove any download attributes or save options from ASCIIPlayer.jsx (ensure no href/download on elements)
- [x] T031 [US4] Add Content-Disposition: inline header to audio endpoint (prevent browser download prompt)

**Checkpoint**: No download mechanism exists for converted content

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T032 [P] Add rate limiting middleware in server/src/api/routes.py (5 req/min upload, 60 req/min other)
- [x] T033 [P] Add conversion timeout handling in server/src/services/converter.py (fail gracefully after 60s)
- [x] T034 [P] Handle edge case: video with no audio track in server/src/services/audio.py (return silent audio stream)
- [x] T035 [P] Handle edge case: corrupted/incomplete uploads in server/src/services/validator.py (reject with clear error)
- [x] T036 [P] Handle edge case: concurrent conversion requests in server/src/services/storage.py (queue or reject)
- [x] T037 Run quickstart.md validation scenarios end-to-end
- [x] T038 Run ruff check + basedpyright on server/
- [x] T039 Run npm test on client/ (if tests added)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies - start immediately
- **Phase 2 (Foundational)**: Depends on Phase 1 completion - BLOCKS all user stories
- **Phase 3 (US1)**: Depends on Phase 2 completion
- **Phase 4 (US2)**: Depends on Phase 2 completion; can run parallel with US1
- **Phase 5 (US3)**: Depends on Phase 2 completion; independent of US1/US2
- **Phase 6 (US4)**: Depends on Phase 2 completion; independent of US1/US2/US3
- **Phase 7 (Polish)**: Depends on all user stories being complete

### User Story Dependencies

- **US1 (Upload/Convert)**: Can start after Phase 2 - No dependencies on other stories
- **US2 (Play)**: Can start after Phase 2 - Needs US1 to exist for full integration, but player component can be built independently
- **US3 (Themes)**: Can start after Phase 2 - Fully independent
- **US4 (No Download)**: Can start after Phase 2 - Fully independent

### Parallel Opportunities

**Phase 1 (Setup)**:
```bash
# T002, T003, T004, T005 can run in parallel (different files)
```

**Phase 2 (Foundational)**:
```bash
# T007, T008, T009, T011 can run in parallel (different files)
```

**After Phase 2**:
```bash
# All 4 user stories can start in parallel:
# Developer A: US1 (Upload/Convert)
# Developer B: US2 (Play)
# Developer C: US3 (Themes)
# Developer D: US4 (No Download)
```

**Within US1**:
```bash
# T012, T013 can run in parallel (converter + audio services)
# T014, T015 can run in parallel (different endpoints)
```

**Within US2**:
```bash
# T019, T020 can run in parallel (different endpoints)
```

**Phase 7 (Polish)**:
```bash
# T032, T033, T034, T035, T036 can run in parallel (different concerns)
```

---

## Implementation Strategy

### MVP First (User Stories 1 + 2)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: US1 (Upload/Convert)
4. Complete Phase 4: US2 (Play)
5. **STOP and VALIDATE**: Test full upload-to-playback flow
6. Deploy/demo if ready

### Incremental Delivery

1. Phase 1 + Phase 2 → Foundation ready
2. Phase 3 + Phase 4 → MVP! Full conversion + playback works
3. Phase 5 → Theme switching added
4. Phase 6 → Download protection added
5. Phase 7 → Polish and edge cases handled
6. Each phase adds value without breaking previous functionality

### Parallel Team Strategy

With multiple developers:
1. Team completes Phase 1 + Phase 2 together
2. Once Phase 2 is done:
   - Developer A: Phase 3 (US1)
   - Developer B: Phase 4 (US2)
   - Developer C: Phase 5 (US3)
   - Developer D: Phase 6 (US4)
3. Stories complete and integrate independently
4. Team reviews and merges Phase 7 together

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- US1 + US2 together form the MVP - both are P1 priority
