<template>
  <v-row justify="center">
    <v-dialog v-model="dialog" persistent max-width="600">
      <v-card>
        <v-toolbar color="primary_dark" flat >
          <v-spacer />
          <v-toolbar-title class="headline white--text"> {{setForm}}</v-toolbar-title>
          <v-progress-linear
            :active="loading"
            indeterminate
            absolute
            bottom
            color = "white"
          ></v-progress-linear>	
          <v-spacer />
        </v-toolbar>
        <v-card-text>            
          
          <v-form v-model="valid" ref="form">
            <v-container>  

              <v-row>
                <v-col> 	

                  <h2>Equipo de UPRM: {{team_}}</h2>
                  
                </v-col>        
              </v-row>          
              <v-row>            
                <v-col              
                  md="12"
                >	

                <h2>Fecha del Evento:*</h2>
                  
                </v-col>
              </v-row>
              <v-row>
                <v-col>                        
                
                <v-date-picker
                  v-model="date_"
                  full-width
                  :landscape="$vuetify.breakpoint.smAndUp"
                  :show-current="true"
                  color="green darken-1"
                  class="mt-4"
                  locale="es-419"
                  :min="min_date"
                  :max="max_date"
                ></v-date-picker>
                  
                </v-col>
              </v-row>

              <v-row>            
                <v-col>
                <h2>Hora del Evento:*</h2>
                  
                </v-col>
              </v-row>
              <v-row>
                <v-col>                  
                
                <v-time-picker 
                  v-model="time_" 
                  :landscape="$vuetify.breakpoint.mdAndUp"
                  color="green darken-1"
                  ></v-time-picker>
                  
                </v-col>
              </v-row>          

              <v-row>
                <v-col              
                  md="12"
                >	

                <h2>Localización:</h2>
                
                </v-col>
              </v-row>
              <v-row justify="center">
                <v-col              
                  md="6"
                > 
                        
                  <v-select
                    v-model="locality_"
                    :items="localities"
                    item-text="text"
                    item-value="value"             
                    label ="Localización*"              
                  ></v-select>            
                </v-col>
              </v-row>

              <v-row justify="center">
                <v-col              
                  md="6"
                >              
                  <v-text-field
                    v-model="venue_"                                    
                    label="Lugar del Evento"
                    required
                    counter="25"
                    :rules="[alphaSpaces('Lugar del Evento')]"
                  ></v-text-field>              
                </v-col>
              </v-row>

              <v-row>
                <v-col             
                  md="12"
                >	

                  <h2>Nombre de Oponente:</h2>
                  
                </v-col>
              </v-row>
              <v-row justify="center">
                <v-col              
                  md="6"
                >              
                  <v-text-field
                    v-model="opponent_name_"                                    
                    label="Oponente"
                    required
                    counter="25"
                    :rules="[generalPhrase('Nombre de Oponente')]"
                  ></v-text-field>              
                </v-col>
              </v-row>

              <v-row>
                <v-col>	

                  <h2>Resumen de Evento:</h2>
                  
                </v-col>

                <v-col              
                  md="9"
                >                
                  <v-textarea
                    v-model="eventSummary_"                      
                    :counter="250"                
                    label="Resumen"
                    auto-grow
                    rows = "2"
                    outlined
                    :rules="[minLength('Resumen',1),maxSummaryLength('Resumen',250)]"
                  ></v-textarea>              
                </v-col>
              </v-row>

              <v-row>
                <v-col>
                   <v-checkbox
                    v-model="terms"
                    label="He revisado mis cambios*."
                  >
                  </v-checkbox>
                </v-col>
              </v-row>
             
            </v-container>
            <small>*indica campo requerido</small>
          </v-form>
        
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
            <v-btn color="grey darken-3" text @click="close()">
             Cerrar
            </v-btn>
           <v-btn 
              color="primary darken-1" 
              text                        
              :disabled="!(valid & terms)"
              @click="submit"
              :loading="editing"
            >
              Guardar
            </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
import { mapActions, mapGetters} from "vuex";
import rules from "@/utils/validations"
export default {

  name: "EditEventModal",
  props:{
    dialog:Boolean,
    date:String,//Date of the event
    time:String,//Time of the event
    locality:Boolean,//Flag of whether the even is local or away
    venue:String,//Venue of the event
    sport_name:String,//Sport of the event
    branch:String,//Branch of the sport of the event
    team_season_year:Number,
    opponent_name:String,
    event_summary:String,
    id:Number,//Id of the event in the database
    trigger:Boolean,

  },
  
  data: () => ({
    ready:false,
    valid:false,//Flag denoting the validity of the contents of the fields with rules
    date_:'',     
    time_:'',
    locality_:Boolean,
    localities:[{'text':'Casa','value':true},{'text':'Afuera','value':false}],
    venue_:'',
    team_:'',	
    terms:false,	
    opponent_name_:'',
    eventSummary_:'',
    loading:true, 
    editing:false,//Used for loading state in edit button.
    min_date:'',
    max_date:'',  
   
    
  }),
   


  methods: {

    ...mapActions({      
      editEvent:"events/editEvent"
    }),
    
    ...rules,
    
    /**
     * Function to be called when an event is edited
     * with valid information and the user presses 
     * the edit button.
     */
    async submit () { 

      this.editing = true
      const event_attributes = {}//Temp Object for the attributes of the event.

      event_attributes['event_date'] = this.date_ + ' ' + this.time_
      event_attributes['is_local'] = this.locality_      
      event_attributes['venue'] = this.venue_
      event_attributes['opponent_name'] = this.opponent_name_
      event_attributes['event_summary'] = this.eventSummary_
      
      //Contruct Object for the vuex action to be called.
      const eventJSON = {'event_id':this.id,'attributes':event_attributes}
      
      //Call vuex action and wait for response
      const response = await this.editEvent(eventJSON)

      this.editing = false
      if(response !== 'error'){
        this.$emit("update:trigger",false)
        this.close()        
      }          
     
    },
    
    /**
     * Formats the content in the edit event form
     * fields.
     */
    format(){
			
      if(this.dialog && !this.ready){       
        
        this.date_ = this.date

        const dateYear = this.team_season_year
        this.min_date = dateYear +'-01-01'
        this.max_date = dateYear+1 +'-12-31'

        this.time_ = this.time     
        
        this.locality_ = this.locality
      
        this.team_ = this.sport_name + '-' + this.branch + '-' + this.team_season_year		        
        
        if(this.venue)
          this.venue_ = this.venue   
        
        if(this.opponent_name)
          this.opponent_name_ = this.opponent_name

        if(this.event_summary)
          this.eventSummary_ = this.event_summary        

        this.ready = true
        this.loading = false    
      }

    },

    /**
     * Closes the EditEventModal and resets optional 
     * fields.
     */
    close(){
      this.ready = false
      this.terms = false
      this.loading = true
      this.$refs.form.resetValidation()
      this.venue_ = ''
      this.opponent_name_ = ''
      this.eventSummary_ = ''
      this.$emit("update:dialog",false);       
    }
       
  }, 

  computed:{
    setForm(){     
      this.format()
      return "Editar Evento"

    }	
  },

 
}
</script>