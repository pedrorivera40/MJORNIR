<template>
  <v-container>
    <v-layout column>
      <v-flex xs12 sm8 md6>
        <div class="text-center">
          <v-row>
            <client-only>
              <v-col>
                <h1 v-if="smAndDown" class="header display-2 my-12">
                  ¡Bienvenido a Huella Deportiva
                  <span class="highlight">Web</span>!
                </h1>
                <h1 v-else-if="mdAndUp" class="header display-3 my-12">
                  ¡Bienvenido a Huella Deportiva
                  <span class="highlight">Web</span>!
                </h1>
                <Logo :width="mdAndUp ? '' : '350px'" />
                <h2 class="my-6 headline">¡Orgullo Colegial!</h2>
              </v-col>
            </client-only>
          </v-row>
        </div>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import Logo from "~/components/Logo.vue";
export default {
  components: {
    Logo
  },
  data() {
    return {
      smAndDown: this.$vuetify.breakpoint.smAndDown,
      mdAndUp: this.$vuetify.breakpoint.mdAndUp
    };
  }
};
</script>

<style lang="scss" scoped>
.header {
  margin-top: 6rem;
  font-size: 3rem;
  .highlight {
    color: #168f09;
  }
}
</style>