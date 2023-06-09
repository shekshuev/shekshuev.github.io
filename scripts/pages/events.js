import { TimeLine } from "../components/time-line.js";
import { TabBar } from "../components/tab-bar.js";
import { EventCard } from "../components/event-card.js";
import { SearchInput } from "../components/search-input.js";
import { useEventsStore } from "../store/use-event-store.js";
import { DefaultLayout } from "../components/default-layout.js";
const { mapState, mapActions } = Pinia;

export const EventsPage = {
    components: { TimeLine, TabBar, EventCard, SearchInput, DefaultLayout },
    template: /*html*/ `
        <tab-bar :tabs="eventTabs" :selected-tab-id="selectedTabId" @tab-clicked="onTabSelected"></tab-bar>
        <default-layout>
            <template v-slot:left>
                <search-input v-model="searchString"></search-input>
                <div class="scrollable">
                    <time-line :events="filteredEvents" @on-event-selected="onEventSelected"></time-line>
                </div>
            </template>
            <template v-slot:right>
                <div class="scrollable">
                    <event-card v-if="selectedEvent" 
                                :event="selectedEvent" 
                                @on-save="onSaveEvent"
                                @on-delete="onDeleteEvent"
                                @on-cancel="onCancelEvent"
                                class="mb-10"></event-card>
                    <button type="button" 
                            v-else
                            @click="onCreateEventButtonClicked"
                            class="w-full md:w-auto text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center">
                            Создать ВКС
                    </button>
                </div>
            </template>
        </default-layout>        
    `,
    data: () => ({
        eventTabs: [
            {
                id: 0,
                title: "Все мероприятия"
            },
            {
                id: 1,
                title: "Прошедшие"
            },
            {
                id: 2,
                title: "Будущие"
            }
        ],
        searchString: "",
        selectedTabId: 0,
        selectedEvent: null
    }),
    computed: {
        ...mapState(useEventsStore, ["events"]),
        filteredEvents() {
            let filtered = [];
            if (this.selectedTabId === 0) {
                filtered = this.events.sort((a, b) => a.beginDate.getTime() - b.beginDate.getTime());
            } else if (this.selectedTabId === 1) {
                const now = Date.now();
                filtered = this.events
                    .filter(e => e.beginDate.getTime() < now)
                    .sort((a, b) => a.beginDate.getTime() - b.beginDate.getTime());
            } else if (this.selectedTabId === 2) {
                const now = Date.now();
                filtered = this.events
                    .filter(e => e.beginDate.getTime() >= now)
                    .sort((a, b) => a.beginDate.getTime() - b.beginDate.getTime());
            }
            return this.searchString.length > 0
                ? filtered.filter(
                      e =>
                          e.title.toLowerCase().indexOf(this.searchString.toLowerCase()) >= 0 ||
                          e.description.toLowerCase().indexOf(this.searchString.toLowerCase()) >= 0
                  )
                : filtered;
        }
    },
    methods: {
        ...mapActions(useEventsStore, ["addEvent", "updateEvent", "removeEvent"]),
        onTabSelected(id) {
            this.selectedTabId = id;
        },
        onEventSelected(event) {
            this.selectedEvent = event;
        },
        onCreateEventButtonClicked() {
            this.selectedEvent = {};
        },
        onSaveEvent(event) {
            if (event.id) {
                this.updateEvent(event);
            } else {
                this.addEvent(event);
            }
            this.selectedEvent = null;
        },
        onDeleteEvent(event) {
            this.removeEvent(event);
            this.selectedEvent = null;
        },
        onCancelEvent() {
            this.selectedEvent = null;
        }
    }
};
